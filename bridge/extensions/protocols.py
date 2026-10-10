"""Finite packet capture and protocol metadata import using bring-your-own tshark."""
import pathlib, tempfile
from common import AnalysisError, local_file, require, result, run
from graphs import protocol

FIELDS = ['frame.number','frame.time_epoch','_ws.col.Protocol','ip.src','ip.dst','ipv6.src','ipv6.dst','tcp.srcport','tcp.dstport','udp.srcport','udp.dstport','http.request.method','http.response.code','http2.streamid','tls.handshake.extensions_server_name']

def packet_metadata(path):
    argv=['tshark','-n','-r',str(path),'-T','fields','-E','separator=/t','-E','occurrence=f']
    for field in FIELDS: argv.extend(['-e',field])
    output=run(argv)
    rows=[]
    for line in output.splitlines():
        values=line.split('\t')
        rows.append({key:value for key,value in zip(FIELDS,values) if value})
    return rows

def inspect_capture(p):
    mode=p.get('format','har')
    if mode=='har':return protocol(p)
    path=local_file(p)
    if mode=='pcap':
        return result({'frames':packet_metadata(path)},'derived',
                      ['Only selected packet metadata is decoded; payloads, authorization headers and cookies are excluded.', 'Encrypted traffic stays encrypted; gRPC/protobuf schema inference is not supplied by packet metadata.'],path)
    if mode=='protobuf':
        # --decode_raw needs stdin bytes; a temporary descriptor-free decode is distinct from schema inference.
        import shutil, subprocess
        if not shutil.which('protoc'):raise AnalysisError('DEPENDENCY_MISSING','Bring your own protoc executable')
        with path.open('rb') as src, tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
            try:r=subprocess.run(['protoc','--decode_raw'],stdin=src,stdout=out,stderr=err,timeout=20)
            except subprocess.TimeoutExpired as e:raise AnalysisError('TIMEOUT','protoc decode exceeded 20 seconds') from e
            if out.tell()>16*1024*1024:raise AnalysisError('RESOURCE_LIMIT','protobuf output exceeds 16 MiB')
            out.seek(0);err.seek(0)
            if r.returncode:raise AnalysisError('PROVIDER_FAILED',err.read(2048).decode(errors='replace'))
            text=out.read().decode(errors='replace')
        # Return only tag and scalar wire-shape observations, never raw values.
        import re
        tags=[]
        for line in text.splitlines():
            m=re.match(r'\s*(\d+)\s*([:{])',line)
            if m:tags.append({'tag':int(m.group(1)),'shape':'nested_candidate' if m.group(2)=='{' else 'scalar_or_bytes'})
        return result({'tag_observations':tags},'inferred',['Descriptor-free decode cannot identify original field names, types or requiredness; nested candidates are ambiguous.'],path)
    raise AnalysisError('INVALID_INPUT','format: har|pcap|protobuf')

def capture(p):
    if p.get('approved') is not True:raise AnalysisError('AUTHORITY_REQUIRED','Approve capture on this explicit interface')
    interface=require(p,'interface')
    duration=p.get('duration',5)
    if not isinstance(duration,(int,float)) or not 0<duration<=10:raise AnalysisError('INVALID_INPUT','duration must be >0 and <=10 seconds')
    argv=['tshark','-n','-i',interface,'-a','duration:'+str(duration),'-c','10000']
    if p.get('filter'):argv+=['-f',require(p,'filter')]
    with tempfile.TemporaryDirectory(prefix='hurea-pcap-') as tmp:
        path=pathlib.Path(tmp)/'capture.pcapng'
        run(argv+['-w',str(path)],timeout=20)
        from common import digest
        data={'interface':interface,'duration_seconds':duration,'frames':packet_metadata(path),'capture_sha256':digest(path)}
    return result(data,'observed',['Network capture is capped at 10 seconds/10,000 packets and needs OS capture authority.', 'Temporary raw capture is deleted after metadata analysis. No interception certificate, TLS bypass or packet injection.'])
