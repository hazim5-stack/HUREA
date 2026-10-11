# Extensions verification record

## Verified locally

- TypeScript strict typecheck and CLI/MCP build.
- Python archive, plist, source Interface Builder XML, HAR schema/redaction, graph,
  SSA IR, fingerprint, firmware signature, local SDK process/registry and malformed-input tests.
- Real Python subprocess execution from the application workflow.
- Canonical Evidence parsing and file SHA-256 binding.
- Cancellation of an active local child provider.
- MCP in-memory SDK client/server handshake, complete extension tool listing,
  actual provider availability response and denied runtime authority response.
- Generated public MCP and product catalogs updated for the added tools.

Final focused verification passed **32 Python tests and 58 Vitest tests (90 total)**.
The Vitest lane includes extension application/MCP execution, original process
ownership invariants, public tool contracts and wire schemas, CLI/product catalog
facts, README consistency and package conformance.
`npm run check:fast` and `npm run docs:check` passed. The build and package file
inventory check passed; optional Python cache files are excluded from distribution.
These checks do not certify optional external tools or physical devices.

The first full `npm run check:pr` test run recorded 1,863 passes, 62 failures and
4 skips. It exposed a legacy environment token in a fixture, missing extension
README rows/CLI argument guidance and inconsistent extension annotations. Those
were corrected and their targeted lanes passed in the final 90-test verification.
The full suite also encountered `listen EPERM` on Unix sockets, unavailable live
process snapshots and provider startup/cleanup failures in existing process and
Hopper/Ghidra tests. The affected Hopper lease and Ghidra client source files match
the input archive. Full-suite passing status is **not claimed**; the full suite
was not rerun after the targeted corrections. Host-dependent lanes need a suitable
machine with socket/process visibility and their own actual provider checks.

## Not verified in this environment

The provider diagnostic reported no Frida, LLDB, JADX, aapt2, LIEF, Rizin, Binwalk,
unsquashfs, tshark, protoc or Binary Ninja. IDA/Hex-Rays and an iPhone/Android device
were not available. Their adapter code is included, but live/toolchain conformance
has not been established here. OpenSSL and nm were present; their mobile provider
modes were not part of the live-tool verification lane.

The original Hopper/Ghidra real-provider verification lanes were not run for this
extension update. Existing mocked/boundary checks do not replace those claims.

## Remaining coverage boundaries

- iOS inspection does not reconstruct compiled SwiftUI layouts, encrypted
  executables, all Swift metadata, or full typed Swift ABI call values.
- Android static matching does not resolve dynamic JNI registrations or infer
  semantic managed/native call chains from coexisting files.
- SSA graph construction consumes explicit analyzer IR; binary-wide automatic
  alias analysis and context/path-sensitive data flow are not supplied.
- Network schemas are sample-derived; protobuf tags are descriptor-free
  candidates, not recovered original field names/types or full gRPC contracts.
- Firmware scans/listing do not extract/emulate all filesystems or infer every
  device service/update mechanism.
- Function similarity is heuristic and does not establish semantic equivalence
  or resolve split/merged functions.
- The local provider SDK is explicitly trusted code execution, not a sandbox,
  signature-verifying package manager or remote plugin marketplace.
- Evidence Studio displays imported labels without verifying those imported
  record identifiers. Evidence newly emitted by the HUREA workflow is canonical.

See `extensions.md` for resource budgets, parameters and cleanup limits.
