"""Run inside IDA; Hex-Rays pseudocode is exported only when licensed/available."""
import json
import ida_auto, ida_funcs, ida_gdl, ida_lines, ida_pro, idautils, idc
ida_auto.auto_wait()
functions = []
try:
    import ida_hexrays
    decompiler = ida_hexrays.init_hexrays_plugin()
except ImportError:
    decompiler = False
for address in idautils.Functions():
    func = ida_funcs.get_func(address)
    item = {'id': hex(address), 'name': idc.get_func_name(address),
            'instructions': [ida_lines.tag_remove(idc.generate_disasm_line(a, 0) or '') for a in idautils.FuncItems(address)],
            'calls': sorted({hex(ref) for a in idautils.FuncItems(address) for ref in idautils.CodeRefsFrom(a, False) if ida_funcs.get_func(ref) and ida_funcs.get_func(ref).start_ea != address}),
            'cfg_edges': [[hex(b.start_ea), hex(s.start_ea)] for b in ida_gdl.FlowChart(func) for s in b.succs()]}
    if decompiler:
        cfunc = ida_hexrays.decompile(address)
        if cfunc: item['pseudocode'] = str(cfunc)
    functions.append(item)
with open(OUTPUT_PATH_PLACEHOLDER, 'w') as out: json.dump({'functions': functions}, out)
ida_pro.qexit(0)
