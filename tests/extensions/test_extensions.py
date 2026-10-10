import contextlib, io, json, os, pathlib, plistlib, subprocess, sys, tempfile, unittest, zipfile
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'bridge/extensions'))
import common, graphs, mobile, providers, runtime, protocols

class ExtensionsTest(unittest.TestCase):
    def setUp(self):
        common.SNAPSHOTS.clear()
        self.temp = tempfile.TemporaryDirectory(); self.root = pathlib.Path(self.temp.name)
    def tearDown(self): self.temp.cleanup()
    def write(self, name, value):
        path = self.root / name; path.write_text(json.dumps(value)); return str(path)
    def archive(self, name, members):
        path = self.root / name
        with zipfile.ZipFile(path, 'w') as z:
            for k,v in members.items(): z.writestr(k,v)
        return str(path)
    def test_apk_inventory(self):
        p = self.archive('a.apk', {'AndroidManifest.xml': 'x','classes.dex':'x','lib/arm64-v8a/a.so':'x','assets/a.js':'x'})
        data = mobile.android({'path':p})['data']
        self.assertTrue(data['manifest_present']); self.assertEqual(data['dex'], ['classes.dex'])
    def test_ios_binary_plist_and_ui(self):
        p = self.archive('a.ipa', {'Payload/A.app/Info.plist':plistlib.dumps({'CFBundleIdentifier':'org.hazim.demo','CFBundleURLTypes':[{'CFBundleURLSchemes':['hurea']} ]},fmt=plistlib.FMT_BINARY), 'Payload/A.app/main.storyboard': '<document><button id="a" title="OK"/></document>'})
        data = mobile.ios({'path':p})['data']
        self.assertEqual(data['bundles'][0]['plist']['CFBundleIdentifier'],'org.hazim.demo')
        self.assertEqual(data['interface_resources'][0]['elements'][1]['attributes']['title'],'OK')
    def test_archive_traversal(self):
        p=self.archive('bad.zip',{'../../escape':'x'})
        with zipfile.ZipFile(p) as z, self.assertRaises(common.AnalysisError): common.extract(z, self.root/'extract')
    def test_archive_duplicate_paths(self):
        p=self.root/'dup.zip'
        with zipfile.ZipFile(p,'w') as z:
            z.writestr('a','x')
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter('ignore');z.writestr('a','y')
        with zipfile.ZipFile(p) as z, self.assertRaises(common.AnalysisError): common.bounded_members(z)
    def test_archive_symlink(self):
        p=self.root/'symlink.zip'
        with zipfile.ZipFile(p,'w') as z:
            info=zipfile.ZipInfo('link');info.external_attr=0o120777<<16;z.writestr(info,'/etc/passwd')
        with zipfile.ZipFile(p) as z, self.assertRaises(common.AnalysisError): common.extract(z,self.root/'ex')
    def test_forward_cycle_and_backward_flow(self):
        p=self.write('flow.json',{'nodes':[{'id':x} for x in 'abcd'],'edges':[{'from':'a','to':'b','kind':'argument'},{'from':'b','to':'c','kind':'return'},{'from':'c','to':'b','kind':'field'}]})
        self.assertEqual(len(graphs.flow({'path':p,'source':'a'})['data']['nodes']),3)
        self.assertEqual(len(graphs.flow({'path':p,'source':'c','direction':'backward'})['data']['nodes']),3)
    def test_flow_dangling(self):
        p=self.write('f.json',{'nodes':[{'id':'a'}],'edges':[{'from':'a','to':'x'}]})
        with self.assertRaises(common.AnalysisError):graphs.flow({'path':p,'source':'a'})
    def test_similarity_relocation_and_empty(self):
        a=self.write('left.json',{'functions':[{'id':'a','instructions':['call 0x123']},{'id':'empty'}]})
        b=self.write('right.json',{'functions':[{'id':'b','instructions':['call 0x456']},{'id':'empty2'}]})
        r=graphs.similarity({'left':a,'right':b})['data']
        self.assertEqual(r['matches'][0]['status'],'same_fingerprint');self.assertEqual(r['unmatched_left'],['empty'])
    def test_similarity_changed(self):
        a=self.write('a.json',{'functions':[{'id':'a','instructions':['add','ret']}]})
        b=self.write('b.json',{'functions':[{'id':'b','instructions':['add','sub','ret']}]})
        self.assertEqual(graphs.similarity({'left':a,'right':b})['data']['matches'][0]['status'],'modified_candidate')
    def har(self,url):return {'log':{'entries':[{'request':{'method':'POST','url':url,'headers':[{'name':'Authorization','value':'VERY_SECRET'}],'postData':{'text':'{"token":"VERY_SECRET","n":1}'}},'response':{'status':200,'content':{'text':'{"ok":true}'},'headers':[]}}]}}
    def test_har_redaction_schema_and_diff(self):
        a=self.write('a.har',self.har('https://u:password@host/order?token=VERY_SECRET'))
        b=self.write('b.har',self.har('https://host/old'))
        out=graphs.protocol({'path':a,'compare':b});encoded=json.dumps(out)
        self.assertNotIn('VERY_SECRET',encoded);self.assertNotIn('password',encoded)
        self.assertEqual(out['data']['observations'][0]['request_schema']['properties']['n']['type'],'integer')
        self.assertEqual(len(out['data']['endpoint_diff']['added']),1)
    def test_schema_mixed_array(self):
        self.assertEqual(len(graphs.schema([True,1,'x',None])['items']['anyOf']),4)
    def test_graph_html_injection(self):
        p=self.write('graph.json',[{'evidence_id':'e1','operation':'</script><script>bad()</script>','confidence':'observed','evidence_links':['missing']}])
        r=graphs.evidence_graph({'path':p})['data'];self.assertTrue(r['edges'][0]['missing'])
        self.assertNotIn('</script><script>bad',r['html']);self.assertIn('\\u003c',r['html'])
    def test_firmware_magic(self):
        p=self.root/'fw.bin';p.write_bytes(b'abc'+b'hsqs'+b'\x00\x7fELF')
        hits=providers.firmware({'path':str(p)})['data']['signature_candidates']
        self.assertEqual([h['offset'] for h in hits],[3,8])
    def test_empty_firmware(self):
        p=self.root/'empty';p.write_bytes(b'')
        self.assertEqual(providers.firmware({'path':str(p)})['data']['signature_candidates'],[])
    def test_provider_status(self):
        self.assertIn('lldb',providers.status({})['data']['executables'])
    def manifest(self,args=None):return {'schema_version':1,'id':'local-demo','executable':sys.executable,'operations':{'inspect':{'args':args or ['-c','import json; print(json.dumps({"ok":True}))','{target}'],'mutates_target':False,'writes_filesystem':False,'accesses_network':False}}}
    def test_sdk_real_local_process(self):
        p=self.write('manifest.json',self.manifest()); target=self.write('target.json',{})
        r=providers.sdk({'path':p,'mode':'run','approved':True,'operation':'inspect','target':target})
        self.assertEqual(r['data']['output'],{'ok':True})
    def test_sdk_atomic_registry_backup(self):
        p=self.write('m.json',self.manifest());registry=str(self.root/'registry.json')
        providers.sdk({'path':p,'mode':'register','approved':True,'registry':registry})
        providers.sdk({'path':p,'mode':'register','approved':True,'registry':registry})
        self.assertTrue(pathlib.Path(registry+'.bak').exists())
    def test_sdk_requires_approval(self):
        p=self.write('m.json',self.manifest())
        with self.assertRaises(common.AnalysisError):providers.sdk({'path':p,'mode':'run'})
    def test_sdk_rejects_missing_effects(self):
        m=self.manifest();del m['operations']['inspect']['writes_filesystem']
        with self.assertRaises(common.AnalysisError):providers.validate_manifest(m)
    def test_sdk_rejects_declared_network(self):
        m=self.manifest();m['operations']['inspect']['accesses_network']=True
        p=self.write('m.json',m)
        with self.assertRaises(common.AnalysisError):providers.sdk({'path':p,'mode':'run','approved':True,'operation':'inspect','target':self.write('t.json',{})})
    def test_runtime_authority(self):
        for fn in (runtime.frida_observe,runtime.lldb_observe):
            with self.assertRaises(common.AnalysisError) as e: fn({'pid':1})
            self.assertEqual(e.exception.code,'AUTHORITY_REQUIRED')
    def test_runtime_bounds(self):
        for p in ({'approved':True,'pid':-1},{'approved':True,'pid':1,'duration':99},{'approved':True,'pid':True}):
            with self.assertRaises(common.AnalysisError):runtime.authority(p)
    def test_dependency_missing(self):
        with self.assertRaises(common.AnalysisError) as e:common.run(['hurea_nonexistent_tool_xyz'])
        self.assertEqual(e.exception.code,'DEPENDENCY_MISSING')
    def test_subprocess_deadline(self):
        with self.assertRaises(common.AnalysisError) as e:common.run([sys.executable,'-c','import time; time.sleep(5)'],timeout=0.1)
        self.assertEqual(e.exception.code,'TIMEOUT')
    def test_artifact_change_detected(self):
        p=self.write('a.json',{});common.local_file({'path':p});pathlib.Path(p).write_text('changed')
        with self.assertRaises(common.AnalysisError) as e:common.result({},path=pathlib.Path(p))
        self.assertEqual(e.exception.code,'ARTIFACT_CHANGED')
    def test_engine_invalid_json(self):
        out=subprocess.run([sys.executable,str(ROOT/'bridge/extensions/engine.py')],input='{bad',capture_output=True,text=True)
        self.assertFalse(json.loads(out.stdout)['ok']);self.assertEqual(out.returncode,0)
    def test_engine_unknown_operation(self):
        out=subprocess.run([sys.executable,str(ROOT/'bridge/extensions/engine.py')],input='{"operation":"invalid"}',capture_output=True,text=True)
        self.assertEqual(json.loads(out.stdout)['error']['code'],'INVALID_INPUT')
    def test_interprocedural_ssa_graph(self):
        p=self.write('ir.json',{'functions':[{'id':'main','parameters':['x'],'instructions':[{'id':'call','kind':'call','callee':'encode','args':['x'],'defs':['y'],'uses':['x']},{'id':'exit','kind':'return','uses':['y']}]},{'id':'encode','parameters':['value'],'instructions':[{'id':'ret','kind':'return','uses':['value']}]}]})
        r=graphs.ir_flow({'path':p})['data']
        self.assertIn('argument',[e['kind'] for e in r['edges']]);self.assertIn('return',[e['kind'] for e in r['edges']]);self.assertEqual(r['unknowns'],[])
    def test_interprocedural_non_ssa_rejected(self):
        p=self.write('ir.json',{'functions':[{'id':'f','parameters':['x'],'instructions':[{'id':'a','defs':['x']}]}]})
        with self.assertRaises(common.AnalysisError):graphs.ir_flow({'path':p})
    def test_capture_requires_approval(self):
        with self.assertRaises(common.AnalysisError) as e:protocols.capture({'interface':'lo'})
        self.assertEqual(e.exception.code,'AUTHORITY_REQUIRED')
    def test_capture_bounds(self):
        with self.assertRaises(common.AnalysisError):protocols.capture({'interface':'lo','approved':True,'duration':60})
    def test_protocol_unknown_format(self):
        p=self.write('wire.bin',{})
        with self.assertRaises(common.AnalysisError):protocols.inspect_capture({'path':p,'format':'wrong'})
if __name__=='__main__':unittest.main()
