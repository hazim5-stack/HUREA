# HUREA Extensions v1

This update adds 14 optional CLI/MCP tools covering the proposed expansion areas.
It is an initial implementation with explicit coverage boundaries, not a claim of complete source recovery or universal device support.
Existing Hopper, Ghidra, browser, Apple native metadata and managed providers remain available.
License terms and source attribution are documented in LICENSE.

## Running an operation

Build with `npm ci` and `npm run build:cached`. Python 3.10+ is required for extensions.
No optional tool or license is installed by HUREA.

```bash
hurea extensions inspect_extension_providers -
hurea extensions inspect_ios_package request.json
```

`request.json` contains the operation parameters directly:

```json
{ "path": "/absolute/path/App.ipa", "mode": "bundle" }
```

The matching MCP call is `inspect_ios_package` with
`{"parameters":{"path":"/absolute/path/App.ipa","mode":"bundle"}}`.
Both surfaces call the same application workflow and return canonical SHA-256 Evidence.
Set `HUREA_EXTENSION_PYTHON` to the Python executable in your Frida/LIEF/Binary Ninja environment.

## Coverage and prerequisites

| Area                        | Implemented                                                                                                                                       | Requirements / limits                                                                                                                  |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Native runtime / Frida      | Modules, threads, finite native calls/backtraces, bounded memory bytes, future RegisterNatives observations, compiled ObjC bridge                 | Python frida; explicitly selected PID/device and `approved:true`; no persistent attach session or typed Swift ABI reconstruction       |
| LLDB                        | Attach snapshot of modules/threads/frames; finite symbol breakpoint trace; detach in cleanup                                                      | LLDB with embedded Python; OS attach permissions; no debugger variable or general memory observer                                      |
| Android                     | ZIP/DEX/native/resource inventory, manifest/badging, JADX source reconstruction, native declarations/loads, exported JNI names                    | aapt2/JADX/nm for respective modes; static export names and declarations are not asserted to be resolved JNI calls                     |
| Apple / iOS                 | Binary/XML plists, bundle and extension settings, provisioning CMS decode, source storyboard/XIB elements, asset inventory, Mach-O symbol listing | OpenSSL/nm where used; profile trust not verified; compiled CAR/NIB/SwiftUI layout not reconstructed; encrypted Mach-O stays encrypted |
| Interprocedural flow        | Build graph from explicit SSA def/use/direct call parameters and returns; traverse forward/backward including field edges                         | Imported analyzer IR or explicit graph; unresolved calls/definitions reported; context-insensitive, alias and path feasibility unknown |
| Protocols                   | HAR sample schemas and endpoint diffs, PCAP metadata, descriptor-free protobuf tag candidates, bounded live packet metadata                       | tshark for PCAP/capture; protoc for protobuf; no TLS bypass or reliable original protobuf field/type reconstruction                    |
| Function similarity         | Normalized instruction/string/constant/call/CFG Jaccard fingerprints, one-to-one candidate matches, changed/unmatched records                     | Imported function JSON; scores are heuristics; split/merge and semantic equivalence unknown                                            |
| Evidence Studio             | Offline interactive SVG graph with operation filter, clickable nodes, confidence/authority/limitations and missing links                          | `build_evidence_graph` returns HTML inline; imports retain their labels and are not verified by this viewer                            |
| Provider SDK                | Manifest inspection, atomic local registration with backup, trusted declared read-only JSON process operations                                    | `manage_local_provider`; explicit approval for registration/run; no automatic npm install or sandbox enforcement                       |
| Firmware                    | SquashFS/UBIFS/DTB/ELF/gzip/ZIP magic offsets, binwalk scan, unsquashfs list                                                                      | binwalk/unsquashfs for external modes; magic candidates are inferred; no automatic extraction/emulation                                |
| Binary Ninja / Rizin / LIEF | Binary inventory; Binary Ninja instructions/calls/CFG export; Rizin info; LIEF imports/exports/sections                                           | Bring your own tool and valid license/Python environment; no licenses bundled                                                          |
| IDA / Hex-Rays              | Functions/instructions/calls/CFG export and pseudocode when Hex-Rays is available                                                                 | Explicit IDA executable and license; temporary target copy; no license bundled                                                         |

## Tool parameters

- `inspect_extension_providers`: `{}`
- `inspect_android_package`: `path`, `mode: inventory|manifest|decompile|jni`.
- `inspect_ios_package`: `path`, `mode: bundle|symbols`.
- `build_interprocedural_graph`: `path` to SSA IR (example below).
- `trace_interprocedural_flow`: `path`, `source`, `direction: forward|backward`.
- `compare_function_fingerprints`: `left`, `right`, `threshold` (0..1, default 0.5).
- `inspect_protocol_capture`: `path`, `format: har|pcap|protobuf`; `compare` for a second HAR.
- `capture_protocol_session`: `interface`, `approved:true`, `duration` (>0 and <=10), optional BPF `filter`.
- `build_evidence_graph`: `path` to an Evidence array or `{evidence:[]}`.
- `inspect_firmware_image`: `path`, `mode: scan|binwalk|squashfs`.
- `inspect_external_binary`: `path`, `engine: lief|rizin|binaryninja|ida`, `python` for Binary Ninja, `executable` for IDA.
- `manage_local_provider`: `path` (manifest), `mode: inspect|register|run`; registration needs `registry` and `approved:true`; run needs `operation`, `target`, `approved:true`.
- `observe_native_runtime`: `pid`, `approved:true`, `mode: modules|threads|trace|memory|jni|objc|swift`, `duration` (>0 and <=10), `max_events` (1..10000). Optional `device_id`; `module`/`symbol` or `address` for trace; `address`/`size` (1..4096) for memory; `class`/`selector` for ObjC. `swift` uses native symbols/addresses rather than type-aware Swift hooks.
- `observe_debugger_runtime`: `pid`, `approved:true`, `mode: snapshot|trace`, `symbol` for trace, `duration` (>0 and <=10).

## Frida ObjC bridge

Modern Frida separates the Objective-C bridge from the basic injected runtime.
Compile `bridge/extensions/objc_agent.js` in your own project containing
`frida-objc-bridge` and `frida-compile`, then provide its output as `agent_path`.
The bridge calls the agent's `rpc.exports.start(parameters)` after loading it.
This executes explicitly selected trusted code in the target.

Example request:

```json
{
  "pid": 1234,
  "approved": true,
  "mode": "objc",
  "class": "UIViewController",
  "selector": "- viewDidAppear:",
  "agent_path": "/absolute/path/objc_agent.compiled.js",
  "duration": 3
}
```

Sessions use finally cleanup to unload scripts/detach. LLDB also enables
`target.detach-on-error`. Host/tool failures or forced termination can prevent cleanup;
do not interpret these measures as proof that every target remains unaffected.

## Interprocedural IR

```json
{
  "functions": [
    {
      "id": "main",
      "parameters": ["input"],
      "instructions": [
        {
          "id": "call",
          "kind": "call",
          "callee": "encode",
          "args": ["input"],
          "defs": ["encoded"],
          "uses": ["input"]
        },
        { "id": "return", "kind": "return", "uses": ["encoded"] }
      ]
    },
    {
      "id": "encode",
      "parameters": ["value"],
      "instructions": [{ "id": "return", "kind": "return", "uses": ["value"] }]
    }
  ]
}
```

Variables must be SSA: one definition per variable per function. Fields can be
represented as explicit graph nodes and field edges. Indirect calls remain unresolved.

## Provider SDK manifest

```json
{
  "schema_version": 1,
  "id": "local-rizin",
  "executable": "rizin",
  "operations": {
    "inspect": {
      "args": ["-q", "-c", "ij", "{target}"],
      "mutates_target": false,
      "writes_filesystem": false,
      "accesses_network": false
    }
  }
}
```

Only declare effects honestly. The SDK is a trusted local extension mechanism,
not a sandbox. Registration stores the manifest path and SHA-256; run currently
accepts an explicitly selected manifest rather than a registry ID. No remote discovery,
automatic install, manifest signature validation or runtime policy enforcement is provided.

## Resource bounds and errors

Requests/results are limited to 16 MiB; input files to 512 MiB; expanded archives
to 1 GiB/50,000 members; parsed Apple resources to 8 MiB. ZIP traversal, symlinks and
duplicate members are rejected during extraction. File-backed observations verify
that selected inputs did not change between selection and evidence creation.
Runtime/capture windows are at most 10 seconds; the outer bridge deadline is 60 seconds.
Unix cancellation terminates the process group, with a forced stop after two seconds.
Windows cancellation only terminates the bridge process; native runtime extensions
are unverified there, and descendant cleanup is not guaranteed.

Missing tools return `DEPENDENCY_MISSING`, unavailable authority returns
`AUTHORITY_REQUIRED`, invalid parameters return `INVALID_INPUT`, and time/output
bounds produce `TIMEOUT`/`RESOURCE_LIMIT`. Providers are not silently installed.

## Verification

Run `npm run test:extensions` for format/graph/protocol/SDK boundary tests, and
Vitest for `ExtensionAnalysis.test.ts` and `extensionsMcp.test.ts` for actual local
subprocess and MCP transport checks. See `EXTENSIONS_VALIDATION.md` for this build's
verified coverage and unverified external/device lanes.

## References

- Frida JavaScript API: https://frida.re/docs/javascript-api/
- Frida bridge packaging: https://frida.re/docs/bridges/
- LLDB Python API: https://lldb.llvm.org/use/python-reference.html
- LIEF binary abstraction: https://lief.re/doc/latest/api/binary_abstraction/python.html
- Android JNI guidance: https://github.com/android/ndk/wiki/JNI
