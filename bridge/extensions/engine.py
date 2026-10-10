#!/usr/bin/env python3
"""HUREA extension bridge. One bounded JSON request on stdin, one JSON response."""
import json, sys, signal

def cancel(signum, frame):
    raise AnalysisError("CANCELLED", "Bridge interrupted")

from common import AnalysisError
from mobile import android, ios
from graphs import flow, similarity, evidence_graph, ir_flow
from protocols import inspect_capture, capture
from providers import status, binary, firmware, sdk
from runtime import frida_observe, lldb_observe
OPERATIONS = {'capture_protocol_session': capture, 'build_interprocedural_graph': ir_flow, 'inspect_extension_providers': status, 'inspect_android_package': android,
              'inspect_ios_package': ios, 'trace_interprocedural_flow': flow,
              'compare_function_fingerprints': similarity, 'inspect_protocol_capture': inspect_capture,
              'build_evidence_graph': evidence_graph, 'inspect_firmware_image': firmware,
              'inspect_external_binary': binary, 'manage_local_provider': sdk,
              'observe_native_runtime': frida_observe, 'observe_debugger_runtime': lldb_observe}

def main():
    signal.signal(signal.SIGTERM, cancel)
    try:
        raw = sys.stdin.buffer.read(16 * 1024 * 1024 + 1)
        if len(raw) > 16 * 1024 * 1024: raise AnalysisError('RESOURCE_LIMIT', 'Request exceeds 16 MiB')
        request = json.loads(raw)
        op = request.get('operation')
        if op not in OPERATIONS: raise AnalysisError('INVALID_INPUT', 'Unknown extension operation')
        params = request.get('parameters', {})
        if not isinstance(params, dict): raise AnalysisError('INVALID_INPUT', 'parameters must be an object')
        value = OPERATIONS[op](params)
        output = json.dumps({'ok': True, 'result': value}, allow_nan=False)
        if len(output.encode()) > 16 * 1024 * 1024: raise AnalysisError('RESOURCE_LIMIT', 'Result exceeds 16 MiB; use a smaller scope')
        print(output)
    except AnalysisError as e:
        print(json.dumps({'ok': False, 'error': {'code': e.code, 'message': str(e)}}))
    except Exception as e:
        print(json.dumps({'ok': False, 'error': {'code': 'ANALYSIS_FAILED', 'message': f'{type(e).__name__}: {e}'}}))
if __name__ == '__main__': main()
