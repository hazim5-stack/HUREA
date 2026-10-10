"""External tool adapters and a local, explicitly trusted provider SDK."""
import importlib.util, json, os, pathlib, shutil, tempfile
from common import AnalysisError, digest, json_file, local_file, require, result, run

TOOLS = ('lldb','jadx','aapt2','apktool','nm','openssl','rizin','binwalk','unsquashfs','tshark','frida-compile','protoc')

def status(p):
    return result({'executables': {n: shutil.which(n) for n in TOOLS},
                   'python_modules': {n: importlib.util.find_spec(n) is not None for n in ('frida','lief','binaryninja')},
                   'policy': 'bring-your-own; no installation or license acquisition'})

def binary(p):
    path = local_file(p)
    engine = p.get('engine', 'lief')
    if engine == 'lief':
        try: import lief
        except ImportError as e: raise AnalysisError('DEPENDENCY_MISSING', 'Install LIEF in the selected Python environment') from e
        b = lief.parse(str(path))
        if b is None: raise AnalysisError('UNSUPPORTED_FORMAT', 'LIEF cannot parse this file')
        data = {'format': type(b).__name__, 'entrypoint': hex(b.entrypoint),
                'sections': [{'name': s.name, 'address': hex(s.virtual_address), 'size': s.size} for s in b.sections],
                'imports': list(b.imported_functions), 'exports': list(b.exported_functions)}
        # LIEF Function objects vary by format/version: stringify structured names when necessary.
        data['imports'] = [x if isinstance(x,str) else x.name for x in data['imports']]
        data['exports'] = [x if isinstance(x,str) else x.name for x in data['exports']]
    elif engine == 'rizin':
        data = json.loads(run(['rizin', '-q', '-c', 'ij', str(path)]))
    elif engine in ('binaryninja', 'ida'):
        with tempfile.TemporaryDirectory(prefix='hurea-provider-') as tmp:
            output = pathlib.Path(tmp) / 'export.json'
            exporter = pathlib.Path(__file__).with_name(engine + '_export.py')
            if engine == 'binaryninja':
                run([p.get('python', 'python3'), str(exporter), str(path), str(output)], timeout=45)
            else:
                executable = require(p, 'executable')
                # IDA may create sidecars; operate only on a temporary copy of the target.
                target = pathlib.Path(tmp) / 'target.bin'; shutil.copyfile(path, target)
                local_exporter = pathlib.Path(tmp) / 'exporter.py'
                local_exporter.write_text(exporter.read_text().replace('OUTPUT_PATH_PLACEHOLDER', repr(str(output))))
                run([executable, '-A', '-S' + str(local_exporter), str(target)], timeout=45)
            if not output.is_file(): raise AnalysisError('PROVIDER_FAILED', 'Provider produced no export')
            data = json.loads(output.read_text())
    else: raise AnalysisError('INVALID_INPUT', 'engine: lief|rizin|binaryninja|ida')
    return result({'engine': engine, 'analysis': data}, limitations=['Coverage follows the installed tool and target format; no decompiler license is installed automatically.'], path=path)

def firmware(p):
    path = local_file(p)
    signatures = {'squashfs-le': b'hsqs', 'squashfs-be': b'sqsh', 'ubifs': b'\x31\x18\x10\x06',
                  'dtb': b'\xd0\x0d\xfe\xed', 'elf': b'\x7fELF', 'gzip': b'\x1f\x8b\x08', 'zip': b'PK\x03\x04'}
    import mmap
    matches = []
    if path.stat().st_size:
        with path.open('rb') as f, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as memory:
            for name, magic in signatures.items():
                offset = memory.find(magic)
                while offset >= 0:
                    matches.append({'kind': name, 'offset': offset, 'confidence': 'inferred'})
                    if len(matches) > 10000: raise AnalysisError('RESOURCE_LIMIT', 'Too many magic candidates')
                    offset = memory.find(magic, offset + 1)
    data = {'signature_candidates': sorted(matches, key=lambda m: m['offset'])}
    if p.get('mode', 'scan') == 'binwalk': data['binwalk'] = run(['binwalk', str(path)])
    elif p.get('mode') == 'squashfs':
        with tempfile.TemporaryDirectory(prefix='hurea-squashfs-') as tmp:
            # List-only avoids writing potentially untrusted embedded filesystem entries.
            data['filesystem_listing'] = run(['unsquashfs', '-ll', str(path)], cwd=tmp)
    elif p.get('mode', 'scan') != 'scan': raise AnalysisError('INVALID_INPUT', 'Firmware mode: scan|binwalk|squashfs')
    return result(data, 'inferred', ['Magic-byte hits are candidates and may be false positives.', 'No automatic firmware execution, extraction or embedded service emulation. SquashFS listing expects a filesystem image starting at offset zero.'], path)

def validate_manifest(m):
    if not isinstance(m, dict) or m.get('schema_version') != 1: raise AnalysisError('INVALID_INPUT', 'Provider schema_version must be 1')
    require(m, 'id'); require(m, 'executable'); require(m, 'operations', dict)
    for op, spec in m['operations'].items():
        if not isinstance(op, str) or not isinstance(spec, dict): raise AnalysisError('INVALID_INPUT', 'Invalid provider operation')
        args = require(spec, 'args', list)
        if not all(isinstance(a, str) for a in args): raise AnalysisError('INVALID_INPUT', 'args must be strings')
        for effect in ('mutates_target', 'writes_filesystem', 'accesses_network'):
            if not isinstance(spec.get(effect), bool): raise AnalysisError('INVALID_INPUT', f'Declare {effect} explicitly')
    return m

def sdk(p):
    mode = p.get('mode', 'inspect')
    path, manifest = json_file(p)
    manifest = validate_manifest(manifest)
    if mode == 'inspect': return result(manifest, path=path)
    if p.get('approved') is not True: raise AnalysisError('AUTHORITY_REQUIRED', 'Explicitly approve this trusted local provider')
    if mode == 'run':
        name = require(p, 'operation')
        spec = manifest['operations'].get(name)
        if spec is None: raise AnalysisError('INVALID_INPUT', 'Operation absent from provider manifest')
        if spec['mutates_target'] or spec['writes_filesystem'] or spec['accesses_network']:
            raise AnalysisError('UNSUPPORTED_AUTHORITY', 'SDK v1 admits declared local read-only operations only; declarations are trust statements, not sandbox enforcement')
        target = local_file(p, 'target')
        argv = [manifest['executable']] + [a.replace('{target}', str(target)) for a in spec['args']]
        output = run(argv)
        return result({'provider': manifest['id'], 'operation': name, 'output': json.loads(output)},
                      limitations=['Executes explicitly trusted provider code outside a sandbox; manifest effect declarations are not independently enforced.'], path=target)
    if mode == 'register':
        registry = pathlib.Path(require(p, 'registry')).resolve()
        value = json.loads(registry.read_text()) if registry.exists() else {'schema_version': 1, 'providers': {}}
        value['providers'][manifest['id']] = {'manifest': str(path), 'sha256': digest(path)}
        registry.parent.mkdir(parents=True, exist_ok=True)
        if registry.exists(): shutil.copyfile(registry, str(registry) + '.bak')
        fd, temp = tempfile.mkstemp(prefix='.hurea-', dir=registry.parent)
        try:
            with os.fdopen(fd, 'w') as f: json.dump(value, f, indent=2)
            os.replace(temp, registry)
        finally:
            if os.path.exists(temp): os.unlink(temp)
        return result({'registry': str(registry), 'provider': manifest['id']}, path=path)
    raise AnalysisError('INVALID_INPUT', 'Provider mode: inspect|register|run')
