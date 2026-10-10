"""Validated local analysis primitives. No shell, network, or automatic installation."""
import hashlib, json, os, pathlib, shutil, subprocess, tempfile, zipfile

SNAPSHOTS = {}

class AnalysisError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code

def require(p, key, kind=str):
    value = p.get(key)
    if not isinstance(value, kind) or (kind is str and not value):
        raise AnalysisError('INVALID_INPUT', f'{key} must be {kind.__name__}')
    return value

def local_file(p, key='path'):
    path = pathlib.Path(require(p, key)).resolve(strict=True)
    if not path.is_file():
        raise AnalysisError('INVALID_INPUT', f'{key} must identify a file')
    if path.stat().st_size > 512 * 1024 * 1024:
        raise AnalysisError('RESOURCE_LIMIT', 'Input file exceeds 512 MiB')
    SNAPSHOTS[str(path)] = digest(path)
    return path

def run(argv, timeout=40, cwd=None):
    if not shutil.which(argv[0]):
        raise AnalysisError('DEPENDENCY_MISSING', f'Bring your own executable: {argv[0]}')
    # Temporary output files prevent unbounded pipe buffering. Never interpolate into a shell.
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        try:
            proc = subprocess.run(argv, stdout=out, stderr=err, timeout=timeout, cwd=cwd)
        except subprocess.TimeoutExpired as e:
            raise AnalysisError('TIMEOUT', f'{argv[0]} exceeded {timeout}s') from e
        for stream in (out, err):
            if stream.tell() > 16 * 1024 * 1024:
                raise AnalysisError('RESOURCE_LIMIT', 'Provider output exceeds 16 MiB')
            stream.seek(0)
        stdout, stderr = out.read().decode('utf-8', 'replace'), err.read().decode('utf-8', 'replace')
    if proc.returncode:
        raise AnalysisError('PROVIDER_FAILED', f'{argv[0]} exited {proc.returncode}: {stderr[:3000]} {stdout[:1000]}')
    return stdout

def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def result(data, confidence='observed', limitations=(), path=None):
    for selected, expected in SNAPSHOTS.items():
        if digest(selected) != expected:
            raise AnalysisError('ARTIFACT_CHANGED', f'Input changed during analysis: {selected}')
    return {'data': data, 'confidence': confidence, 'limitations': list(limitations),
            'subject': None if path is None else {'path': str(path), 'sha256': digest(path)}}

def json_file(p, key='path'):
    path = local_file(p, key)
    if path.stat().st_size > 16 * 1024 * 1024:
        raise AnalysisError('RESOURCE_LIMIT', 'JSON input exceeds 16 MiB')
    return path, json.loads(path.read_text(encoding='utf-8'))

def bounded_members(z):
    members = z.infolist()
    if len(members) > 50000 or sum(i.file_size for i in members) > 1024 * 1024 * 1024:
        raise AnalysisError('RESOURCE_LIMIT', 'Archive exceeds 50,000 members or 1 GiB expanded bytes')
    if len({i.filename for i in members}) != len(members):
        raise AnalysisError('INVALID_INPUT', 'Duplicate archive paths are ambiguous')
    return members

def extract(z, directory):
    root = pathlib.Path(directory).resolve()
    for i in bounded_members(z):
        target = (root / i.filename).resolve()
        if not target.is_relative_to(root) or i.filename.startswith('/') or '\\' in i.filename:
            raise AnalysisError('INVALID_INPUT', 'Unsafe archive path')
        if (i.external_attr >> 16) & 0o170000 == 0o120000:
            raise AnalysisError('INVALID_INPUT', 'Archive symlinks are unsupported')
        if not i.is_dir():
            target.parent.mkdir(parents=True, exist_ok=True)
            with z.open(i) as src, target.open('wb') as dst:
                shutil.copyfileobj(src, dst)
