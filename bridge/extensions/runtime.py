"""Finite native observation sessions with explicit local target authority."""
import base64, json, pathlib, tempfile, threading, time
from common import AnalysisError, require, result, run

def authority(p):
    if p.get('approved') is not True:
        raise AnalysisError('AUTHORITY_REQUIRED', 'Set approved=true for this explicit PID and runtime operation')
    pid = require(p, 'pid', int)
    if isinstance(pid, bool) or pid <= 0: raise AnalysisError('INVALID_INPUT', 'pid must be positive')
    duration = p.get('duration', 2)
    if not isinstance(duration, (int, float)) or not 0 < duration <= 10:
        raise AnalysisError('INVALID_INPUT', 'duration must be >0 and <=10 seconds')
    return pid, duration

def frida_observe(p):
    pid, duration = authority(p)
    try: import frida
    except ImportError as e: raise AnalysisError('DEPENDENCY_MISSING', 'Install frida in the selected Python environment') from e
    mode = p.get('mode', 'modules')
    if mode not in ('modules', 'threads', 'trace', 'memory', 'jni', 'objc', 'swift'):
        raise AnalysisError('INVALID_INPUT', 'Unknown Frida mode')
    cap = p.get('max_events', 1000)
    if not isinstance(cap, int) or not 1 <= cap <= 10000: raise AnalysisError('INVALID_INPUT', 'max_events must be 1..10000')
    script = '''const p = PARAMS;let count=0;const cap=p.max_events||1000;
function emit(x){if(count++<cap)send(x)}
function hook(address,name){Interceptor.attach(address,{onEnter(args){emit({event:'enter',name,address:address.toString(),thread:Process.getCurrentThreadId(),args:[0,1,2,3].map(i=>args[i].toString()),backtrace:Thread.backtrace(this.context,Backtracer.ACCURATE).map(x=>DebugSymbol.fromAddress(x).toString())})},onLeave(ret){emit({event:'leave',name,return_pointer:ret.toString(),thread:Process.getCurrentThreadId()})}})}
if(p.mode==='modules')emit(Process.enumerateModules().map(m=>({name:m.name,path:m.path,base:m.base.toString(),size:m.size})));
else if(p.mode==='threads')emit(Process.enumerateThreads().map(t=>({id:t.id,state:t.state})));
else if(p.mode==='memory'){const n=p.size||256;emit({address:p.address,hex:Array.from(new Uint8Array(ptr(p.address).readByteArray(n))).map(b=>b.toString(16).padStart(2,'0')).join('')})}
else if(p.mode==='trace'||p.mode==='swift'){const a=p.address?ptr(p.address):Process.getModuleByName(p.module).getExportByName(p.symbol);hook(a,p.symbol||p.address);emit({event:'ready'})}
else if(p.mode==='objc'){if(typeof ObjC==='undefined')throw Error('ObjC bridge unavailable; provide agent_path compiled with frida-objc-bridge');const m=ObjC.classes[p.class][p.selector];hook(m.implementation,p.class+' '+p.selector);emit({event:'ready'})}
else if(p.mode==='jni'){const matches=Process.getModuleByName('libart.so').enumerateSymbols().filter(s=>s.name.includes('RegisterNatives')&&!s.name.includes('CheckJNI'));if(!matches.length)throw Error('RegisterNatives symbol unavailable');for(const m of matches)Interceptor.attach(m.address,{onEnter(args){const n=args[3].toInt32();if(n<0||n>4096)return;for(let i=0;i<n;i++){const a=args[2].add(i*Process.pointerSize*3);emit({event:'jni_registration',name:a.readPointer().readUtf8String(),signature:a.add(Process.pointerSize).readPointer().readUtf8String(),function:a.add(Process.pointerSize*2).readPointer().toString()})}}});emit({event:'ready'})}
'''.replace('PARAMS', json.dumps({**p, 'mode': mode}))
    if mode in ('trace', 'swift'):
        if not p.get('address'):
            require(p, 'module'); require(p, 'symbol')
    if mode == 'objc': require(p, 'class'); require(p, 'selector')
    if mode == 'memory':
        require(p, 'address')
        if not isinstance(p.get('size', 256), int) or not 1 <= p.get('size', 256) <= 4096:
            raise AnalysisError('INVALID_INPUT', 'Memory size must be 1..4096')
    device = frida.get_local_device() if not p.get('device_id') else frida.get_device(require(p, 'device_id'), timeout=5)
    events, errors, dropped = [], [], [0]
    session, loaded = None, None
    def on_message(message, data):
        if message.get('type') == 'error': errors.append(message.get('description', 'Agent failed'))
        elif len(events) < cap: events.append(message.get('payload'))
        else: dropped[0] += 1
    try:
        session = device.attach(pid)
        if p.get('agent_path'):
            # An explicitly selected trusted compiled agent; this executes code in the target.
            script = pathlib.Path(require(p, 'agent_path')).read_text()
        loaded = session.create_script(script)
        loaded.on('message', on_message); loaded.load()
        if p.get('agent_path'): loaded.exports_sync.start({**p, 'mode': mode})
        if mode in ('trace', 'jni', 'objc', 'swift'): threading.Event().wait(duration)
        else: threading.Event().wait(0.2)
        if errors: raise AnalysisError('PROVIDER_FAILED', '; '.join(errors))
    finally:
        try:
            if loaded is not None: loaded.unload()
        finally:
            if session is not None: session.detach()
    return result({'pid': pid, 'mode': mode, 'events': events, 'event_cap': cap, 'cap_reached': len(events) >= cap, 'host_dropped': dropped[0]},
                  limitations=['Attaching/instrumenting may affect target timing and code pages.', 'Trace captures four raw argument pointers, not decoded types; event order is callback delivery order.', 'Swift uses explicit native export/address and does not recover Swift ABI values.', 'JNI capture sees future RegisterNatives calls only; JNI class identity is unresolved.', 'Frida agent caps emissions; cap_reached means the trace may be truncated.'])

def lldb_observe(p):
    pid, duration = authority(p)
    encoded = base64.b64encode(json.dumps(p).encode()).decode()
    with tempfile.TemporaryDirectory(prefix='hurea-lldb-') as tmp:
        script = pathlib.Path(tmp) / 'snapshot.py'
        template = pathlib.Path(__file__).with_name('lldb_session.py').read_text()
        script.write_text(template.replace('PARAMETERS_BASE64', encoded))
        output = run(['lldb', '--batch', '-o', 'command script import ' + str(script)], timeout=25)
    records = [line.split('HUREA_JSON:', 1)[1] for line in output.splitlines() if 'HUREA_JSON:' in line]
    if not records: raise AnalysisError('PROVIDER_FAILED', 'LLDB returned no observation')
    data = json.loads(records[-1])
    if data.get('error'): raise AnalysisError('PROVIDER_FAILED', data['error'])
    return result(data, limitations=['LLDB temporarily stops the process; breakpoint tracing changes timing.', 'Captures modules, threads and frames, not a general memory or variable reconstruction.', 'Host attach permissions and platform code-signing rules still apply.'])
