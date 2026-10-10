"""Explicit data-flow, heuristic similarity, protocol and Evidence graphs."""
import collections, hashlib, html, json, math, re
from common import AnalysisError, json_file, require, result

def flow(p):
    path, graph = json_file(p)
    nodes, edges = graph['nodes'], graph['edges']
    ids = {n['id'] for n in nodes}
    if len(ids) != len(nodes): raise AnalysisError('INVALID_INPUT', 'Duplicate node IDs')
    if len(nodes) > 50000 or len(edges) > 200000: raise AnalysisError('RESOURCE_LIMIT', 'Graph too large')
    source, direction = require(p, 'source'), p.get('direction', 'forward')
    if source not in ids or direction not in ('forward', 'backward'): raise AnalysisError('INVALID_INPUT', 'Unknown source or direction')
    adj = collections.defaultdict(list)
    for e in edges:
        if e['from'] not in ids or e['to'] not in ids: raise AnalysisError('INVALID_INPUT', 'Dangling edge')
        a, b = (e['from'], e['to']) if direction == 'forward' else (e['to'], e['from'])
        adj[a].append((b, e))
    seen, queue, reached = {source}, collections.deque([source]), []
    while queue:
        a = queue.popleft()
        for b, e in adj[a]:
            reached.append(e)
            if b not in seen: seen.add(b); queue.append(b)
    return result({'nodes': [n for n in nodes if n['id'] in seen], 'edges': reached, 'direction': direction}, 'derived',
                  ['Reachability follows explicit imported def-use/argument/return/field edges; alias resolution and path feasibility are not inferred.', 'This adapter does not automatically construct interprocedural def-use edges from binaries.'], path)

def signature(f):
    tokens = set()
    for key in ('instructions', 'strings', 'constants', 'calls', 'cfg_edges'):
        for item in f.get(key, []):
            s = json.dumps(item, sort_keys=True)
            if key == 'instructions': s = re.sub(r'0x[0-9a-fA-F]+', '<address>', s)
            tokens.add(key + ':' + s)
    return tokens

def similarity(p):
    left_path, left = json_file(p, 'left')
    right_path, right = json_file(p, 'right')
    left, right = left['functions'], right['functions']
    if len(left) * len(right) > 1000000: raise AnalysisError('RESOURCE_LIMIT', 'Comparison exceeds one million pairs')
    for fs in (left, right):
        if len({f['id'] for f in fs}) != len(fs): raise AnalysisError('INVALID_INPUT', 'Duplicate function ID')
    threshold = p.get('threshold', 0.5)
    if not isinstance(threshold, (float, int)) or not 0 <= threshold <= 1: raise AnalysisError('INVALID_INPUT', 'threshold must be 0..1')
    pairs = []
    for a in left:
        for b in right:
            sa, sb = signature(a), signature(b)
            score = len(sa & sb) / len(sa | sb) if sa | sb else 0
            if score >= threshold and sa and sb: pairs.append((score, a['id'], b['id'], sa == sb))
    used_a, used_b, matches = set(), set(), []
    for score, a, b, same in sorted(pairs, key=lambda v: (-v[0], v[1], v[2])):
        if a in used_a or b in used_b: continue
        used_a.add(a); used_b.add(b)
        matches.append({'left': a, 'right': b, 'similarity': score, 'status': 'same_fingerprint' if same else 'modified_candidate'})
    return result({'matches': matches, 'unmatched_left': [f['id'] for f in left if f['id'] not in used_a],
                   'unmatched_right': [f['id'] for f in right if f['id'] not in used_b],
                   'right_subject': {'path': str(right_path), 'sha256': __import__('common').digest(right_path)}}, 'inferred',
                  ['Jaccard token similarity is a heuristic, not probability or proof of semantic equivalence.', 'Greedy one-to-one matching does not resolve split/merged functions. Empty fingerprints remain unmatched.'], left_path)

def schema(v):
    if v is None: return {'type': 'null'}
    if isinstance(v, bool): return {'type': 'boolean'}
    if isinstance(v, str): return {'type': 'string'}
    if isinstance(v, (int, float)): return {'type': 'integer' if isinstance(v, int) else 'number'}
    if isinstance(v, dict): return {'type': 'object', 'properties': {k: schema(x) for k, x in v.items()}}
    if isinstance(v, list):
        variants = {json.dumps(schema(x), sort_keys=True) for x in v}
        return {'type': 'array', 'items': {'anyOf': [json.loads(x) for x in sorted(variants)]} if variants else {}}
    raise AnalysisError('INVALID_INPUT', 'Non-JSON schema value')

def protocol(p):
    from urllib.parse import urlsplit, parse_qsl, urlencode, urlunsplit
    path, har = json_file(p)
    data = []
    def clean_url(url):
        parsed = urlsplit(url)
        host = parsed.hostname or ''
        if parsed.port: host += ':' + str(parsed.port)
        return urlunsplit((parsed.scheme, host, parsed.path, urlencode([(k, '[REDACTED]') for k, _ in parse_qsl(parsed.query)]), ''))
    for e in har['log']['entries']:
        req, resp = e['request'], e['response']
        item = {'method': req['method'], 'url': clean_url(req['url']), 'status': resp['status'],
                'request_header_names': sorted({h['name'] for h in req.get('headers', [])}),
                'response_header_names': sorted({h['name'] for h in resp.get('headers', [])})}
        for label, body in [('request', req.get('postData', {})), ('response', resp.get('content', {}))]:
            text = body.get('text')
            if isinstance(text, str) and body.get('encoding') != 'base64':
                try: item[label + '_schema'] = schema(json.loads(text))
                except json.JSONDecodeError: item[label + '_schema'] = {'unknown': 'not JSON'}
        data.append(item)
    if p.get('compare'):
        _, other = json_file(p, 'compare')
        before = {(e['request']['method'], clean_url(e['request']['url'])) for e in other['log']['entries']}
        after = {(e['method'], e['url']) for e in data}
        delta = {'added': sorted(after - before), 'removed': sorted(before - after)}
    else: delta = None
    return result({'observations': data, 'endpoint_diff': delta}, 'derived',
                  ['Schemas describe captured samples; required fields and complete API contracts are unknown.', 'Header values, cookies, JSON scalar values and query values are omitted. Paths can still contain local identifiers.', 'HAR import only: no live interception, TLS bypass, gRPC/protobuf inference or PCAP decoding.'], path)

def evidence_graph(p):
    path, bundle = json_file(p)
    records = bundle if isinstance(bundle, list) else bundle.get('evidence', bundle.get('records', []))
    ids = {e['evidence_id'] for e in records}
    if len(ids) != len(records): raise AnalysisError('INVALID_INPUT', 'Duplicate evidence IDs')
    nodes = [{'id': e['evidence_id'], 'operation': e.get('operation'), 'confidence': e.get('confidence'),
              'authority': e.get('authority'), 'limitations': e.get('limitations', [])} for e in records]
    edges = [{'from': e['evidence_id'], 'to': ref, 'missing': ref not in ids}
             for e in records for ref in e.get('evidence_links', [])]
    # Embedded JSON escapes < to prevent script termination or HTML injection.
    payload = json.dumps({'nodes': nodes, 'edges': edges}).replace('<', '\\u003c')
    page = '''<!doctype html><meta charset="utf-8"><title>HUREA Evidence Studio</title>
<style>body{font:15px system-ui;background:#111827;color:#e5e7eb;margin:30px}button,input{padding:10px;margin:8px}svg{background:#192338;width:100%;height:650px}text{fill:white;font-size:12px}circle{cursor:pointer}pre{white-space:pre-wrap}</style>
<h1>HUREA Evidence Studio</h1><p>Click a node to inspect its authority and limitations. Imported records are not cryptographically verified by this viewer.</p><input id="q" placeholder="Filter by operation"><svg id="g" viewBox="0 0 1000 650"></svg><pre id="detail"></pre><script>
const graph=PAYLOAD;const colors={observed:'#22c55e',derived:'#3b82f6',inferred:'#f59e0b'};
function draw(){const g=document.getElementById('g');g.replaceChildren();const ns='http://www.w3.org/2000/svg';let nodes=graph.nodes.filter(n=>(n.operation||'').includes(document.getElementById('q').value));let pos=new Map(nodes.map((n,i)=>[n.id,[90+(i%5)*190,50+Math.floor(i/5)*90]]));g.setAttribute('viewBox',`0 0 1000 ${Math.max(650,Math.ceil(nodes.length/5)*90)}`);
function el(tag,attrs){let e=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));g.append(e);return e}
for(let e of graph.edges){let a=pos.get(e.from),b=pos.get(e.to);if(a&&b)el('line',{x1:a[0],y1:a[1],x2:b[0],y2:b[1],stroke:'#64748b'})}
for(let n of nodes){let [x,y]=pos.get(n.id);let c=el('circle',{cx:x,cy:y,r:17,fill:colors[n.confidence]||'#64748b'});c.onclick=()=>document.getElementById('detail').textContent=JSON.stringify(n,null,2);el('text',{x:x-80,y:y+35}).textContent=(n.operation||n.id).slice(0,27)}}document.getElementById('q').oninput=draw;draw();</script>'''.replace('PAYLOAD', payload)
    return result({'nodes': nodes, 'edges': edges, 'html': page}, 'derived', ['Viewer preserves imported labels; Evidence IDs are verified only by the HUREA core, not this import adapter.'], path)

def ir_flow(p):
    """Construct explicit interprocedural edges from caller-supplied SSA IR."""
    path, program=json_file(p)
    nodes,edges=[],[]
    functions={f['id']:f for f in program['functions']}
    if len(functions)!=len(program['functions']):raise AnalysisError('INVALID_INPUT','Duplicate IR function ID')
    definitions={}
    instructions={}
    for f in functions.values():
        fid=f['id'];defs={}
        for name in f.get('parameters',[]):
            key=fid+':param:'+name
            if name in defs:raise AnalysisError('INVALID_INPUT','Duplicate SSA parameter')
            defs[name]=key;nodes.append({'id':key,'function':fid,'variable':name,'kind':'parameter'})
        for ins in f.get('instructions',[]):
            key=fid+':ins:'+ins['id']
            if key in instructions:raise AnalysisError('INVALID_INPUT','Duplicate instruction ID')
            instructions[key]=ins;nodes.append({'id':key,'function':fid,'kind':ins.get('kind','instruction')})
            for var in ins.get('defs',[]):
                if var in defs:raise AnalysisError('INVALID_INPUT','Input must be SSA: duplicate variable definition')
                defs[var]=key
        definitions[fid]=defs
    unknown=[]
    for fid,f in functions.items():
        defs=definitions[fid]
        for ins in f.get('instructions',[]):
            key=fid+':ins:'+ins['id']
            for var in ins.get('uses',[]):
                if var in defs:edges.append({'from':defs[var],'to':key,'kind':'def-use','variable':var})
                else:unknown.append({'instruction':key,'variable':var,'reason':'missing definition'})
            if ins.get('kind')=='call':
                callee=functions.get(ins.get('callee'))
                if callee is None:unknown.append({'instruction':key,'reason':'unresolved callee'});continue
                args=ins.get('args',[]);params=callee.get('parameters',[])
                if len(args)!=len(params):unknown.append({'instruction':key,'reason':'argument count mismatch'});continue
                for arg,param in zip(args,params):
                    if arg in defs:edges.append({'from':defs[arg],'to':callee['id']+':param:'+param,'kind':'argument','callsite':key})
                    else:unknown.append({'instruction':key,'variable':arg,'reason':'missing argument definition'})
                for returned in callee.get('instructions',[]):
                    if returned.get('kind')=='return':
                        edges.append({'from':callee['id']+':ins:'+returned['id'],'to':key,'kind':'return','callsite':key})
    if len(nodes)>50000 or len(edges)>200000:raise AnalysisError('RESOURCE_LIMIT','IR graph too large')
    return result({'nodes':nodes,'edges':edges,'unknowns':unknown},'derived',
                  ['Constructed from explicit SSA definitions and direct call bindings; indirect calls, aliasing and path feasibility remain unknown.', 'Graph is context-insensitive; paths can cross separate callsites. Import SSA IR from your analyzer; binary IR extraction is provider-specific.'],path)
