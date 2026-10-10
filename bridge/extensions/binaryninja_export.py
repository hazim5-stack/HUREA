"""Use with a licensed Binary Ninja Python environment."""
import json, sys
import binaryninja as bn
with bn.load(sys.argv[1]) as bv:
    functions = []
    for f in bv.functions:
        functions.append({'id': hex(f.start), 'name': f.name,
                          'instructions': [''.join(t.text for t in tokens) for tokens, address in f.instructions],
                          'calls': [hex(c.start) for c in f.callees],
                          'cfg_edges': [[hex(b.start), hex(e.target.start)] for b in f.basic_blocks for e in b.outgoing_edges]})
    with open(sys.argv[2], 'w') as out: json.dump({'functions': functions}, out)
