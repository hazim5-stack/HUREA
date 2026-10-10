"""Runs in LLDB's embedded Python, never in the ordinary interpreter."""
import base64, json, time, signal
import lldb

def __lldb_init_module(debugger, internal_dict):
    def cancelled(signum, frame): raise RuntimeError('LLDB observation cancelled')
    signal.signal(signal.SIGTERM, cancelled)
    debugger.HandleCommand('settings set target.detach-on-error true')
    p = json.loads(base64.b64decode('PARAMETERS_BASE64'))
    debugger.SetAsync(True)
    target = debugger.CreateTarget('')
    process = None
    data = {'modules': [], 'threads': [], 'hits': []}
    try:
        error = lldb.SBError()
        process = target.AttachToProcessWithID(debugger.GetListener(), p['pid'], error)
        if error.Fail(): raise RuntimeError(error.GetCString())
        for m in target.module_iter():
            data['modules'].append({'path': str(m.GetFileSpec()), 'uuid': m.GetUUIDString()})
        def frames(t):
            return {'id': t.GetThreadID(), 'frames': [{'function': f.GetFunctionName(), 'pc': hex(f.GetPC())} for f in t]}
        data['threads'] = [frames(t) for t in process]
        if p.get('mode') == 'trace':
            name = p.get('symbol')
            if not isinstance(name, str) or not name: raise RuntimeError('symbol is required for LLDB trace')
            bp = target.BreakpointCreateByName(name)
            if bp.GetNumLocations() == 0: raise RuntimeError('Breakpoint symbol has no resolved locations')
            process.Continue()
            end = time.monotonic() + p.get('duration', 2)
            while time.monotonic() < end and len(data['hits']) < 1000:
                state = process.GetState()
                if state == lldb.eStateStopped:
                    thread = process.GetSelectedThread()
                    if thread.GetStopReason() != lldb.eStopReasonBreakpoint:
                        data['other_stop_reason'] = thread.GetStopReason(); break
                    data['hits'].append(frames(thread)); process.Continue()
                elif state in (lldb.eStateExited, lldb.eStateDetached): break
                time.sleep(0.01)
            target.BreakpointDelete(bp.GetID())
        elif p.get('mode', 'snapshot') != 'snapshot': raise RuntimeError('LLDB mode: snapshot|trace')
    except Exception as e:
        data['error'] = str(e)
    finally:
        if process is not None and process.IsValid() and process.GetState() not in (lldb.eStateExited, lldb.eStateDetached):
            if process.GetState() == lldb.eStateRunning: process.Stop()
            detached = process.Detach()
            if detached.Fail(): data['error'] = 'Detach failed: ' + str(detached)
        print('HUREA_JSON:' + json.dumps(data))
