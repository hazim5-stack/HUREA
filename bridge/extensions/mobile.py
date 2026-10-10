"""Android decoding and Apple bundle/resource inspection."""
import json, pathlib, plistlib, re, tempfile, zipfile, xml.etree.ElementTree as ET
from common import AnalysisError, bounded_members, extract, local_file, require, result, run

def android(p):
    path = local_file(p)
    with zipfile.ZipFile(path) as z:
        names = [i.filename for i in bounded_members(z)]
    mode = p.get('mode', 'inventory')
    data = {'dex': [n for n in names if n.endswith('.dex')],
            'native_libraries': [n for n in names if n.endswith('.so')],
            'resources': [n for n in names if n.startswith(('res/', 'assets/'))],
            'manifest_present': 'AndroidManifest.xml' in names}
    if mode == 'manifest':
        data['manifest_xmltree'] = run(['aapt2', 'dump', 'xmltree', str(path), '--file', 'AndroidManifest.xml'])
        data['badging'] = run(['aapt2', 'dump', 'badging', str(path)])
    elif mode in ('decompile', 'jni'):
        with tempfile.TemporaryDirectory(prefix='hurea-jadx-') as tmp:
            run(['jadx', '--no-res', '-d', tmp, str(path)], timeout=45)
            methods, loads, links = [], [], []
            for f in pathlib.Path(tmp).rglob('*.java'):
                text = f.read_text(errors='replace')
                for n, line in enumerate(text.splitlines(), 1):
                    loc = {'source': str(f.relative_to(tmp)), 'line': n}
                    if re.search(r'\bnative\s+\S+\s+\w+\s*\(', line):
                        methods.append({**loc, 'declaration': line.strip()})
                    if 'loadLibrary(' in line or 'System.load(' in line:
                        loads.append({**loc, 'expression': line.strip()})
                    for match in re.finditer(r'https?://[^\s"<>]+', line):
                        links.append({**loc, 'url': match.group(0)})
            data.update(native_declarations=methods, native_loads=loads, url_candidates=links)
            if mode == 'decompile':
                data['sources'] = [{'path': str(f.relative_to(tmp)), 'text': f.read_text(errors='replace')}
                                   for f in pathlib.Path(tmp).rglob('*.java')]
            if mode == 'jni':
                with zipfile.ZipFile(path) as z:
                    extract(z, pathlib.Path(tmp) / 'apk')
                exports = []
                for n in data['native_libraries']:
                    output = run(['nm', '-D', '--defined-only', str(pathlib.Path(tmp) / 'apk' / n)])
                    exports.extend({'library': n, 'symbol': line.split()[-1]}
                                   for line in output.splitlines() if 'Java_' in line)
                data['jni_exports'] = exports
    elif mode != 'inventory':
        raise AnalysisError('INVALID_INPUT', 'Android mode: inventory|manifest|decompile|jni')
    return result(data, limitations=['Native declarations and exported JNI names are separate observations; dynamic RegisterNatives mappings require runtime evidence.', 'JADX output is reconstructed Java, not original Kotlin/Java source.'], path=path)

def plain(value):
    if isinstance(value, bytes): return {'bytes_hex': value.hex()}
    if isinstance(value, dict): return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [plain(v) for v in value]
    if value is None or isinstance(value, (str, int, float, bool)): return value
    return str(value)

def ios(p):
    path = local_file(p)
    bundles, profiles, interfaces, assets = [], [], [], []
    with zipfile.ZipFile(path) as z:
        members = bounded_members(z)
        for i in members:
            n = i.filename
            if n.endswith(('Info.plist', '.entitlements', 'embedded.mobileprovision', '.storyboard', '.xib')) and i.file_size > 8 * 1024 * 1024:
                raise AnalysisError('RESOURCE_LIMIT', 'Parsed Apple resource exceeds 8 MiB')
            if n.endswith('Info.plist') or n.endswith('.entitlements'):
                if i.file_size > 8 * 1024 * 1024: raise AnalysisError('RESOURCE_LIMIT', 'Plist exceeds 8 MiB')
                bundles.append({'path': n, 'plist': plain(plistlib.loads(z.read(i)))})
            elif n.endswith('embedded.mobileprovision'):
                with tempfile.TemporaryDirectory(prefix='hurea-profile-') as tmp:
                    f = pathlib.Path(tmp) / 'profile'; f.write_bytes(z.read(i))
                    decoded = run(['openssl', 'cms', '-verify', '-inform', 'DER', '-noverify', '-in', str(f)])
                    profiles.append({'path': n, 'profile': plain(plistlib.loads(decoded.encode()))})
            elif n.endswith(('.storyboard', '.xib')):
                root = ET.fromstring(z.read(i))
                interfaces.append({'path': n, 'elements': [{'tag': e.tag, 'attributes': dict(e.attrib)} for e in root.iter()]})
            elif n.endswith(('.car', '.nib', '.storyboardc')) or '/Assets.xcassets/' in n:
                assets.append(n)
        data = {'bundles': bundles, 'provisioning': profiles, 'interface_resources': interfaces,
                'compiled_ui_assets': assets, 'frameworks': sorted({n.filename.split('.framework/')[0]+'.framework' for n in members if '.framework/' in n.filename})}
        if p.get('mode', 'bundle') == 'symbols':
            with tempfile.TemporaryDirectory(prefix='hurea-ios-') as tmp:
                extract(z, tmp)
                symbols = []
                for b in bundles:
                    executable = b['plist'].get('CFBundleExecutable')
                    if isinstance(executable, str):
                        f = (pathlib.Path(tmp) / b['path']).parent / executable
                        if not f.resolve().is_relative_to(pathlib.Path(tmp).resolve()): raise AnalysisError('INVALID_INPUT', 'Unsafe CFBundleExecutable')
                        if f.is_file():
                            symbols.append({'path': str(f.relative_to(tmp)), 'nm': run(['nm', str(f)])})
                data['symbols'] = symbols
        elif p.get('mode', 'bundle') != 'bundle':
            raise AnalysisError('INVALID_INPUT', 'iOS mode: bundle|symbols')
    return result(data, limitations=['Encrypted App Store executables cannot be decompiled by this adapter.', 'SwiftUI layout, runtime class metadata, compiled Assets.car and storyboardc are not reconstructed by bundle inspection.', 'CMS decoded with -noverify; profile signature/trust is not verified.'], path=path)
