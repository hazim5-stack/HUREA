# Changelog

## 3.2.1 (2026-10-03)


### Bug Fixes

* **release:** tolerate npm registry propagation delay (726b730)


### Tests

* **release:** accept guarded npm publishing (b7bc855)

## 3.2.0 (2026-10-03)


### Features

* **native:** add investigation features (#486) (ed933d1)


### Bug Fixes

* **artifacts:** stabilize extraction approval (7eb1a95)
* **browser:** reject unknown Electron input fields (1860d4f)
* **ci:** retain artifacts for delayed reruns (07888ec)
* **cli:** remove ignored result limits (f3645aa)
* consolidate boundary ownership and cleanup failure paths (#477) (2160d4f)
* **contracts:** align byte read schema with provider (f580d9d)
* **ghidra:** return complete native analysis results (a66e43a)
* **managed:** retain every source location (33b2099)
* **process:** capture complete host probe output (6c68ff5)
* **runtime:** make observed target role optional (593a8e1)
* **runtime:** retain complete reconciled graph content (bedd55a)


### Code Refactoring

* **analysis:** remove caller-selected result caps (a8c58c6)
* **analysis:** remove fixed result quotas (20152a9)
* **artifacts:** consolidate inventory into inspection (0fe96d9)
* **artifact:** simplify extraction and inventory results (07ff8b3)
* **artifacts:** remove duplicate inventory wrapper (aa6eee1)
* **artifacts:** remove selectors and traversal quotas (8c24272)
* **artifacts:** select extraction by logical path (7ba3580)
* **browser:** remove arbitrary capture ceilings (5dd3b46)
* **browser:** return complete observation evidence (0e2738f)
* **browser:** return complete scenario observations (e80fe41)
* **browser:** share authorized main-frame polling (eec75ce)
* **browser:** share canonical identity digest (a6d9e49)
* **contracts:** remove duplicate schema aliases (4593c29)
* **contracts:** simplify workflows and drop readiness tool (7acac61)
* **coverage:** evaluate inline without workspaces (9e76054)
* **domain:** encode comparison and lifecycle states exactly (#473) (d65730c)
* **domain:** share AST property name reader (4f4cc59)
* **electron:** retain complete active observations (e8c56e0)
* **errors:** remove stale workspace failures (f570d40)
* **evidence:** remove obsolete ID resolvers (a3920e2)
* **evidence:** remove session ledger quotas (dca293a)
* **files:** use caller paths for local evidence files (c34efca)
* **ghidra:** remove redundant schema markers (c2a6f4b)
* **javascript:** remove analysis ceilings (9aec690)
* **managed:** derive inspection from PE CLI extents (dfad09e)
* **mcp:** simplify evidence and workflows (6740ed5)
* **mcp:** simplify tool inputs and inline results (f55c2b9)
* **mcp:** simplify workflow and observation scope (34d00fd)
* **observation:** internalize capture budgets (7b3c797)
* **observation:** retain complete tool results (fa2b6c5)
* **observation:** return complete inventories (c523c38)
* **permission:** remove unused authorization helpers (1b0ab75)
* **process:** remove fixed scenario ceilings (abf7c11)
* **process:** remove redundant schema version markers (b3aca52)
* **process:** remove request count ceilings (f2dc749)
* **process:** remove unused paired experiment (e1d755f)
* **prompts:** make tool workflows optional (3fd9650)
* **reference:** share graph index projections (6ee87fb)
* remove cross-version investigation workflow (81996df)
* **replay:** share sandbox probe arguments (9fca6c0)
* **replay:** simplify runtime value checks (60cb68a)
* return complete analysis results inline (a2a3243)
* return complete tool results inline (0d96275)
* **runtime:** retain complete reconciliation outputs (79ea571)
* **schema:** remove data-only version markers (5457f4a)
* **server:** remove registration alias (8097ec4)
* **server:** use canonical elicitation type (bb6a58c)
* **test:** colocate pure-domain tests and reduce test debt (#471) (e91c8c3)
* **test:** keep coverage at behavioral boundaries (#474) (d4dc940)
* **tools:** remove arbitrary workflow ceilings (5f73cb0)
* **tools:** remove artificial analysis ceilings (2f08c7c)
* **tools:** remove redundant limits and acknowledgements (bd0e341)
* **tools:** remove remaining arbitrary workflow caps (ecf3ed8)
* **tools:** return complete analysis results inline (2a6eb41)
* **workflows:** simplify evidence reference inputs (24e1fa9)


### Documentation

* add HUREA tool design guidance (#485) (36aeec9)
* clarify aggregate context tools (c7e207c)
* clarify MCP tool design guidance (36aeec9)
* correct inline evidence and Hopper behavior (bf9cce1)
* describe complete application analysis outputs (271b162)
* generalize reverse-engineering workflow (#488) (4ecc7a7)
* improve GitHub issue and pull request templates (c490d85)
* prioritize reusable analysis primitives (#493) (9dd72c4)
* refresh managed conformance manifest (23e56c5)
* refresh tool catalog and cleanup audit fixtures (53db3a4)
* regenerate tool and evidence catalogs (2f604a3)
* regenerate tool and evidence catalogs (f2bbd59)
* **tools:** clarify complete inline results (3b64c81)
* **tools:** clarify complete inline workflows (4168174)
* **tools:** describe uncapped tool behavior accurately (4cea84d)
* **tools:** update inline workflow guidance (4ad937c)


### Tests

* **artifacts:** exercise argument-free extraction preflight (a6d5b3e)
* **browser:** assert strict inputs without legacy fields (9ddf22e)
* **browser:** cover complete screenshot output (3f547ea)
* **browser:** remove stale input field assertion (60c110d)
* **cli:** consolidate duplicate setup journey (9bd7e2c)
* **cli:** remove duplicate browser discovery case (dcb0362)
* **conformance:** remove fixture generator test option (ea853ce)
* **contracts:** remove duplicate tool inventories (0ae3c08)
* **hopper:** name regex search assertion accurately (9240bd8)
* **hopper:** remove dossier identity assertion (b5c0b5b)
* **mcp:** align workflow assertions with current guidance (f8bb113)
* **mcp:** consolidate catalog inventory checks (3afcd64)
* **mcp:** validate defaults at tool boundary (21241d2)
* remove duplicate export schema acceptance (b783e7f)
* remove obsolete schema version assertions (fe342fa)
* remove stale limits and handoff expectations (acf33d6)
* remove vacuous and duplicate assertions (56e2bf7)
* remove Vitest config test exports (d6e545c)
* replace brittle workflow and readme checks (b3529aa)
* replace implementation lock-in with behavioural assertions (#498) (7ee3f23)
* **replay:** remove duplicate schema coverage (4ec2343)

## 3.1.0 (2026-08-09)


### Features

* **electron:** add autonomous Electron runtime analysis (#464) (8f229ed)


### Bug Fixes

* **ci:** guard Release Please PR branch parsing (84cc819)
* **ci:** guard release PR branch parsing (6838b6b)
* harden evidence lifecycle and MCP contracts (5155924)
* harden structured configuration comparisons (#467) (6901edc)
* **npm:** preserve explicit setup versions (#465) (1783bf6)


### Code Refactoring

* **mcp:** make analysis states unrepresentable (#468) (b8a9da0)


### Documentation

* clarify agent reverse-engineering promise (ed4a628)
* clarify the agent reverse-engineering promise (#466) (ed4a628)
* **npm:** simplify current setup command (#469) (8b62b1a)

## 3.0.0 (2026-08-01)


### ⚠ BREAKING CHANGES

* export_evidence_bundle now requires a filesystem path and no longer returns an inline bundle.

### Features

* make evidence bundles canonical MCP resources (1712e6d)


### Bug Fixes

* address MCP resource review feedback (f3b3fb0)
* align aggregate tools with session capabilities (ede91ff)
* **ci:** align Vitest project worker budgets (f47ee1a)
* **ci:** allow documented public type aliases (97f6a0f)
* **ci:** make coverage report merging composable (788f405)
* **ci:** stabilize Vitest project routing and shards (f07acde)
* **errors:** preserve actionable analysis diagnostics (0f96bf3)
* **mcp:** clarify routing and advertise input examples (969519c)
* **mcp:** clarify target routing and caller diagnostics (3e1e8cd)
* **test:** bound boundary worker pressure (935721d)
* **test:** honor boundary ownership and public aliases (92a1c33)
* **test:** retain subprocess coverage and cleanup (7f46bb1)
* **test:** retain subprocess coverage and cleanup (dae2b9c)
* **test:** stabilize boundary timing (f0d8cda)
* **verify:** follow dynamic Hopper tool availability (281e41f)


### Code Refactoring

* preserve provider-neutral runtime seams (a8161f0)


### Documentation

* document resource snapshot workflow (2a45d8d)
* refresh generated SDK metadata (c824db1)
* refresh managed completion manifest (59d4659)


### Tests

* **contracts:** cover validation branches (8ccdb33)
* derive MCP SDK identity expectations (ab4193c)
* **eval:** cover navigation and address tool routing (ba098f2)
* overhaul deterministic suite architecture (48053d1)
* overhaul deterministic suite architecture (513d9b1)
* **package:** verify npx upgrade on published releases (7b6f7be)
* **package:** verify npx upgrade on published releases (1f8ad7b)


### Continuous Integration

* document deterministic suite ownership (3c42403)

## 2.7.0 (2026-07-28)


### Features

* **bytecode:** add JVM and Python bytecode providers (1a75f8d)
* **bytecode:** add JVM and Python bytecode providers (4e0127d), closes #367
* **conformance:** add portable conformance export package format (91fb87d)
* **conformance:** add portable conformance export package format (4ee30e4)
* **metadata:** add deeper ObjC/Swift metadata and database save/licensing (4602efd)
* **metadata:** add deeper ObjC/Swift metadata and database save/licensing (d7a0753), closes #353
* **mobile:** add Android APK/AAB/DEX and iOS IPA static investigation providers (18624df)
* **mobile:** add Android APK/AAB/DEX and iOS IPA static investigation providers (fdeeb27), closes #366
* **package:** add MSIX/MSI/AppX package, resource, and signature analysis (0ef1b91)
* **package:** add MSIX/MSI/AppX package, resource, and signature analysis (6c03f83), closes #363
* **pe:** add broader PE/COFF/PDB static inspection (f942558)
* **pe:** add broader PE/COFF/PDB static inspection (94e6600), closes #362
* **process:** replace procfs sampling with event-backed process-tree capture (a5e355a)
* **process:** replace procfs sampling with event-backed process-tree capture (d5d2e56), closes #332
* **protocol:** add custom TCP/UDP/IPC/XPC and auth-flow capture (1fb22b4)
* **protocol:** add custom TCP/UDP/IPC/XPC and auth-flow capture (6fa6f9b), closes #365
* **protocol:** add gRPC/Protobuf and JSON-RPC/MessagePack capture (54153ed)
* **protocol:** add gRPC/Protobuf and JSON-RPC/MessagePack capture (3f336fe), closes #364


### Bug Fixes

* **catalog:** digest provider projections (645668b)
* **catalog:** digest provider projections (c4cd033)

## 2.6.0 (2026-07-26)


### Features

* complete evidence-backed roadmap workflows (1a0931b)
* **hopper:** report bridge progress diagnostics (7a43420)
* **native:** inspect API boundaries with evidence (521139d)


### Bug Fixes

* **setup:** refresh stale local npx bootstrap (6d37efe)
* **setup:** refresh stale local npx bootstrap (90bb161)


### Performance Improvements

* **mcp:** reduce cold-start work (8ec9bb1)
* **mcp:** reduce cold-start work (fecddc0)


### Tests

* add critical provider workflow coverage (4716fa2)
* **hopper:** remove brittle diagnostic source assertion (40bf55b)
* **investigation:** prove multi-version fixture closure (5184816)
* **mcp:** stabilize lazy-loading verification (7157ab0)
* **package:** prove artifact cleanup and identity (9522adf)

## 2.5.1 (2026-07-25)


### Bug Fixes

* **ci:** normalize generated release metadata (d43a461)
* **ci:** normalize release pull request metadata (119954c)


### Performance Improvements

* **browser:** lazy-load Playwright sessions (305e729)
* **dotnet:** reuse authenticated artifact snapshots (c5e8871)
* eliminate repeated work in analysis hot paths (fbe442b)
* **evidence:** validate ledger mutations incrementally (809dfbf)
* **javascript:** reuse parsed source across analyses (adc4852)
* **server:** cache advertised JSON schemas (6743644)

## 2.5.0 (2026-07-24)


### Features

* add runtime reconstruction roadmap workflows (1dbb157)
* **analysis:** add bounded memory and call tracing (8e7709d)
* **artifacts:** add provider-neutral inspection (d997728)
* **browser:** capture controlled Playwright scenarios (1ac3118)
* **browser:** compare scenario and storage evidence (f27dd74)
* **javascript:** compare source with shipped bundles (697be94)
* **javascript:** recover runtime semantic effects (38c883b)
* **process:** support explicit stdin closure (205bf15)
* **reconstruction:** add obligation ledgers (9d48ca7)
* **reconstruction:** evaluate end-to-end readiness (38ff741)
* **runtime:** add passive V8 Inspector observation (8271650)
* **server:** advertise available tools dynamically (035e114)


### Bug Fixes

* **analysis:** report call-edge truncation (6039b92)
* **browser:** close scenario containment gaps (1bd65f6)
* **browser:** contain scenario pages and preserve inputs (24b3dc4)
* **browser:** require storage fingerprint approval (f0069cb)
* **ci:** allow slower real browser startup (095c75d)
* **ci:** propagate readiness verifier failures (9f9f9c3)
* **ci:** repair cross-platform package verification (1c9e508)
* **comparison:** preserve uncertainty and v1 inputs (b9217dc)
* **hopper:** add bounded analysis recovery (e0bc7fd)
* **javascript:** keep digestless bundle matches unknown (5a76aaf)
* **process:** expose launcher identity mismatch (62ac73c)
* **process:** normalize macOS launcher identity (9c3aec8)
* **process:** tolerate exit during ownership revalidation (a0f8b72)
* **reconstruction:** authenticate obligation proof boundaries (7b1e3bd)
* **reconstruction:** bind proof evidence to claims (83b3368)
* **runtime:** preserve deterministic context identity (9bd2ac5)
* **test:** use direct Node launcher on macOS (13f3372)


### Performance Improvements

* **test:** speed up local and CI validation (1546a8d)
* **test:** speed up local and CI validation (42fbbb2)


### Code Refactoring

* **application:** reuse graph evidence resolution (4e8aa98)
* **browser:** centralize scenario metadata budgeting (e79e367)
* **browser:** clarify inspector capture identifiers (ca035a7)
* **browser:** reuse CDP endpoint parsing (00abf45)
* **javascript:** centralize source range comparison (c9500d3)
* **javascript:** share semantic call-site lookup (94a2c60)
* **reconstruction:** isolate ledger coverage (4f62695)
* **server:** reuse availability policy type (eeb4349)


### Documentation

* document roadmap analysis workflows (f29f683)
* refresh generated roadmap metadata (f904668)


### Tests

* **browser:** use neutral scenario fixture identifiers (fd25a7e)
* **package:** stabilize fake Hopper ownership (0b70131)


### Continuous Integration

* verify runtime observation and readiness (9349ff5)

## 2.4.0 (2026-07-23)


### Features

* **artifacts:** support MSIX and AppX packages (6e6cce1)
* expand reactive capture and package analysis (9da1794)
* **process:** add reactive capture scenarios (69761e9)


### Bug Fixes

* **capabilities:** expose typed availability codes (b906def)

## 2.3.0 (2026-07-23)


### Features

* complete HUREA remediation program (d25e98c)
* **evidence:** generate verifier completion ledgers (c02d33f)
* **evidence:** generate verifier completion ledgers (f5b3e22)
* **javascript:** add bounded semantic relation graph (b3939ea)
* **javascript:** add bounded semantic tracing (56c1a66)
* **javascript:** add local semantic call flow (a26a1c7)
* **javascript:** expose bounded semantic tracing (508a9cc)
* **process:** add bounded reactive scenario domain (42f3b9c)
* **process:** add bounded reactive scenario domain (d34463c)
* **process:** add direct replay machine runner (3df9a07)
* **process:** compare declared concurrent traces (d81745c)
* **process:** coordinate reactive capture effects (b874efd)
* **process:** coordinate reactive capture effects (db9a831)
* **process:** record global capture event order (8bcdb98)
* **process:** record provider and verifier run lineage (02b01d4)
* **process:** record provider and verifier run lineage (513fa29)
* **process:** run finite-state replay during capture (820af60)
* **process:** run finite-state replay during capture (34c583a)


### Bug Fixes

* **browser:** redact transitional target titles (f6095cb)
* **cli:** retain bundled skill and bias setup wizard toward apply (5692b3f)
* **cli:** retain bundled skill and bias setup wizard toward apply (fec5c3c)
* **cli:** route JavaScript applications from analyze (737940c)
* **cli:** route JavaScript applications from analyze (74965d9)
* **javascript:** preserve candidate trace ambiguity (8678b57)
* **knip:** ignore ps binary and in-file schema exports (9960982)
* **mcp:** preserve investigation input policy (5a908a0)
* **mcp:** preserve investigation input policy (f4156d9)
* **process:** bound trace comparison semantics (b4df565)
* **process:** normalize resize frame timestamps (74d1c7b)
* **process:** normalize resize frame timestamps (77696df)
* **process:** preserve nonconforming differences (f1cc485)
* **process:** preserve replay event causality (d895e49)
* **process:** protect unrelated Hopper during cleanup (81539c4)
* **process:** protect unrelated Hopper during cleanup (e4ee4c9)


### Code Refactoring

* **process:** extract capture journal recorder (a32b988)
* **process:** split trace comparison domain logic (75d5a87)
* **process:** split trace comparison helpers (6d8ecd2)


### Documentation

* **cli:** clarify setup consent comment (e869137)
* refresh Node 24 TypeDoc output (846193c)


### Tests

* **browser:** stabilize real shape capture (bb2e243)


### Continuous Integration

* remove redundant typecheck, lint, and format compatibility jobs (eb27f01)
* remove redundant typecheck, lint, and format compatibility jobs (aeb5cb3)
* shard coverage tests and skip docs-only suites (c736317)
* shard coverage tests and skip docs-only suites (fa58082)

## 2.2.0 (2026-07-20)


### Features

* **artifacts:** project mobile application inventories (c6a1a93)
* **artifacts:** project mobile application inventories (d36b385)
* **process:** add bounded replay state machines (fea965b)
* **process:** add bounded replay state machines (dc0c2e5)
* **process:** compare repeatable paired experiments (e9899c0)
* **process:** compare repeatable paired experiments (9ab7aa3)
* streamline agent integration and MCP routing (02cb20b)
* streamline agent integration and MCP routing (3e3d458)


### Bug Fixes

* align session filters and Hopper verification (d7d6bdf)
* **artifacts:** align projection provider targets (560dbda)
* **artifacts:** bound mobile projection candidates (0cc9d46)
* **ci:** keep tool kind type internal (b9bead2)
* **ci:** retry published package verification (0810486)
* **ci:** retry published package verification (c379455)


### Documentation

* refresh generated API links (a2089a4)
* update application projection API (b0cb28a)
* update paired process experiment API (a222327)
* update replay machine API (d74f897)


### Tests

* budget CLI output variant subprocesses (8d3587b)
* cap workers across all hosts (bc80359)
* inherit root options in Vitest projects (168100e)
* isolate slow filesystem and CLI suites (c2e134b)
* stabilize subprocess-heavy integration suites (a556e94)

## 2.1.0 (2026-07-18)


### Features

* add managed characterization and coverage closure (1943496)
* add managed characterization and reconstruction coverage (02c913b)
* **cli:** add explicit package-runner setup wizard (891a11f)
* **cli:** improve setup onboarding (4851449)
* **cli:** improve setup onboarding (16002ff)
* **cli:** support package-name setup wizard (1b90e7f)
* **doctor:** admit the Windows x64 Ghidra boundary (32dda0c)
* **dotnet:** add BYO ILSpy oracle diagnostics (aa200ce)
* **ghidra:** add authenticated Windows loopback transport (629ffc3)
* **ghidra:** bind imports to admitted target bytes (be19c3f)
* **ghidra:** define the Windows P0 admission boundary (6b1fd16)
* **ghidra:** inspect Windows headless installations (86e44be)
* **ghidra:** launch bounded Windows headless sessions (bc0fb45)
* harden authority and runtime conformance boundaries (b537ebf)
* **javascript:** add binding and constant-value semantic IR (3ea8523)
* **javascript:** add binding and constant-value semantic IR (3d71bb5)
* **javascript:** add webpack and rspack runtime adapters (7bccb7c)
* **javascript:** add webpack and rspack runtime adapters (44c7017)
* **javascript:** recover commonjs and esm module relationships (9766fc0)
* **javascript:** recover commonjs and esm module relationships (6c41791)
* **permissions:** add scoped process capture elicitation (e6cfce3)
* **skill:** rename skill to hurea-reverse-engineering (9356634)
* **target:** classify Windows PE admission metadata (24274fe)
* **windows:** define native authority boundary (a1a6b42)


### Bug Fixes

* **build:** preserve native generated-file line endings (00a3078)
* **ci:** remove retired native rebuild steps (2d22731)
* **ci:** validate packaged Windows CLI commands exactly (43418ee)
* **cli:** require explicit setup selections (992ec50)
* **contracts:** make agent-facing schemas self-describing (0df11dd)
* **dotnet:** admit real CLI GUID and fat CIL bodies (735973b)
* **dotnet:** correct CLI pointer and byref signatures (1387be0)
* **dotnet:** correct CLI pointer and byref signatures (fb9ff56)
* **dotnet:** downgrade truncated CIL identity and coverage (736a4e1)
* **dotnet:** downgrade truncated CIL identity and coverage (dae6807)
* **electron:** keep missing unpacked ASAR entries unavailable (fb6964a)
* **electron:** resolve package and dirname entrypoints by context (4847fc4)
* **electron:** resolve package and dirname entrypoints by context (1ac9a09)
* **ghidra:** preserve native endpoint diagnostics (5970a71)
* **ghidra:** preserve Windows batch invocation semantics (0ac418d)
* **ghidra:** validate Windows control characters explicitly (4dccbec)
* **managed:** emit valid x64 conformance PE (dcd94f1)
* **managed:** emit valid x64 conformance PE (c52a822)
* **managed:** preserve page incompleteness in graph and comparison (a6f02a0)
* **managed:** preserve page incompleteness in graph and comparison (8ee0f04)
* **mcp:** clarify advertised schema fields (1581e40)
* **npm:** use latest entry points without install scripts (34252f5)
* **npm:** use latest entry points, remove install scripts, and rename skill (bf85ee6)
* preserve optional unknown filters (db1efef)
* remove unused boundary exports (49f1ec1)
* satisfy dead-code and generated-doc checks (b15a9ec)
* **setup:** preserve onboarding after refactor (da48033)
* **skill:** disclose retired skill cleanup (4c69e61)


### Code Refactoring

* **adapters:** split oversized provider workflows (1a99a60)
* **app:** split session and CLI workflows (c6ee004)
* **domain:** split analysis boundaries (e2c868c)
* finish lint cleanup (2bea405)
* **managed:** split metadata analysis (20c88dd)
* **setup:** keep planner helpers private (2d1f961)
* simplify authorization boundaries (2e5b443)
* simplify doctor and error projections (37f4ac6)
* **skill:** keep only the canonical skill identity (a7c1e87)
* **skill:** remove legacy skill compatibility (8cf0dd2)
* split oversized analysis workflows (af2399e)
* split oversized analysis workflows (3e61a63)
* **windows:** keep capability outcomes module-private (585f523)


### Documentation

* **cli:** describe every command input (d4be3e7)
* **ghidra:** define the experimental Windows P0 (8b5ae41)
* **managed:** align normalized CIL claims with shipped v1 semantics (9a92a79)
* **managed:** align normalized CIL claims with shipped v1 semantics (3f788e9)
* normalize inherited source paths (d33213a)
* preserve generated source links (2ea375f)
* prioritize agent usability in tool design (ad17fe7)
* refresh Electron path resolution API (734a4ef)
* refresh generated API reference (f5f653b)
* regenerate managed coverage API with Node 24 (e47c00e)


### Tests

* add limit monotonicity and partial-evidence regressions (2cce98c)
* add limit monotonicity and partial-evidence regressions (4afd970)
* **ci:** guard Windows Ghidra workflow isolation (81ed68f)
* **ci:** guard Windows Ghidra workflow isolation (98540c8)
* **cli:** cover package-name binary alias (40e2f94)
* **hopper:** add semantic runtime conformance (da1da3b)
* **package:** align setup preflight contract (b33ebb1)


### Continuous Integration

* **ghidra:** add Windows P0 acceptance and real-engine lanes (0b35510)

## 2.0.0 (2026-07-16)


### ⚠ BREAKING CHANGES

* **mcp:** require Evidence for managed reconstruction
* **mcp:** comparison tools now require session-owned Evidence IDs or approved bundle paths, and structured Evidence results use compact references.

### Features

* **application:** add cross-layer graph workflows (778b995)
* **application:** add isolated JavaScript replay (d86231a)
* **dotnet:** add managed artifact triage (c251c38)
* **dotnet:** add managed member comparison (55794d6)
* **dotnet:** add managed member inspection (98cad37)
* **dotnet:** add managed native boundary inspection (466b1bb)
* **dotnet:** add managed runtime correlation planning (5f66cfd)
* **dotnet:** import managed reconstructions (c506664)
* **dotnet:** verify managed native boundaries (8cbc125)
* **electron:** map static process and IPC boundaries (3fa2304)
* **electron:** reconcile static artifacts with passive runtime (8c67dbd)
* **managed:** project static evidence into application graph (6194c1a)
* **managed:** project static evidence into application graph (77178bb)
* **mcp:** harden contracts and evidence references (ee1cd40)
* **mcp:** require Evidence for managed reconstruction (d36af5d)
* **setup:** verify installed skill catalog identity (b2d1f2a)


### Bug Fixes

* **deps:** run freshness check from escaped paths (8a1c128)
* **mcp:** align runtime unknown argument validation (d1e7220)
* **mcp:** hide managed workflows without a session (412bbaf)
* **mcp:** integrate managed contracts after rebase (9c4a93d)
* **mcp:** normalize inferred field descriptions (a807471)
* **mcp:** parse adapter inputs exactly once (37c0f39)
* **mcp:** remove arbitrary schema byte gate (fd08025)
* **mcp:** remove schema byte compaction (f728295)
* **package:** accept expected doctor diagnostics (0f2d013)
* **test:** make host fixtures portable (f23f529)


### Code Refactoring

* **mcp:** remove obsolete managed evidence parser (f7aa191)


### Documentation

* **analysis:** define managed-code evidence boundary (80faff3)
* **api:** refresh managed reconstruction contracts (2b06433)
* **dotnet:** refresh managed reconstruction api (cc1e47c)
* refresh application workflow API links (4a30820)
* refresh managed native verification api (849c052)
* refresh managed runtime api docs (798631a)
* refresh runtime reconciliation API (87b2348)
* **security:** define controlled replay authority (461990d)
* stabilize replay API source links (a8c1057)


### Tests

* **dotnet:** add managed conformance verifier (2b75fcf)
* **dotnet:** verify managed app graph manifests (5be4051)
* **dotnet:** verify managed app graph manifests (a5e5c68)
* **dotnet:** verify managed app manifests (793a948)
* **hopper:** avoid scheduler-sensitive exit timing (6e6827c)
* **mcp:** cover strict compact wire contracts (8de25d0)
* **mcp:** derive sessionless managed inventory (cab7c4a)
* **replay:** use portable seam executables (3183f47)

## 1.7.0 (2026-07-15)


### Features

* **artifact:** reconstruct JavaScript application structure (aa46abf)
* **domain:** add versioned JavaScript Application Graph (2ca5672)
* **ghidra:** add function analysis and conformance (d8321de)
* **ghidra:** add private headless provider session (f0e625d)
* **ghidra:** implement read-only inventory operations (b1c07dd)
* **session:** add explicit provider registry and target binding (941d710)


### Bug Fixes

* address setup, upgrade, and process test regressions (960d759)
* address setup, upgrade, and process test regressions (02f12b9)
* **cli:** make clean source checkouts start reliably (ed17e76)
* **cli:** make clean source checkouts start reliably (6ba9765)
* **setup:** replace managed Hopper on reinstall (0ca93f9)


### Code Refactoring

* **domain:** remove provider-specific target and snapshot state (21da71e)
* **process:** extract reusable provider lifecycle primitives (70e1a0f)


### Documentation

* **api:** refresh profile source anchors (bd3cf96)
* **api:** refresh provider source anchors (a7621c2)
* **architecture:** define provider selection and analysis profiles (75f8696)
* **architecture:** define provider selection and analysis profiles (f9f2fbe)
* reconcile product documentation with shipped behavior (addc208)
* reconcile product documentation with shipped behavior (54056a9)
* refresh Ghidra inventory API links (a45de27)
* regenerate JavaScript graph API with Node 24 (da4817a)


### Tests

* keep package setup verification read-only (acaf030)

## 1.6.0 (2026-07-14)


### Features

* add web and Electron reverse-engineering workflows (be76f80)


### Bug Fixes

* **application:** add explicit investigation replay (7112e1e)
* **application:** add explicit investigation replay (a6b5ca4)
* **browser:** keep page endpoint type internal (3743962)
* **browser:** observe direct target disconnects (9be24f8)
* **browser:** preserve operation-aware cancellation errors (0aac8aa)
* **browser:** support page-scoped CDP transports (c4930f4)
* **browser:** support page-scoped CDP transports (bf96192)
* **browser:** support relative source map URLs (5231e95)
* **cli:** confirm project grant revocation (6397e54)
* **cli:** confirm project grant revocation (7a4cfb4)
* **cli:** restrict production MCP dispatch (8bd0e5f)
* **cli:** restrict production MCP dispatch (190e5d3)
* **doctor:** honor explicit Hopper launcher (c69fe2c)
* **doctor:** honor explicit Hopper launcher (9208592)
* **evidence:** enforce the combined record limit (c791802)
* **evidence:** enforce the combined record limit (834c70c)
* **hopper:** cancel startup before closing (f471a63)
* **hopper:** cancel startup before closing (6cc2fdf)
* **hopper:** select verified Linux demo mode explicitly (46e4052)
* **hopper:** select verified Linux demo mode explicitly (04c5fd6)
* **native:** harden command capture edge cases (c2e64a4)
* **native:** harden command capture edge cases (d39f98d)
* preserve setup diagnostics and clean Knip config (2d1e021)
* preserve setup diagnostics and clean Knip config (5a7ccef)
* **process:** gate sampling on initialized PTY root (57938a8)
* **process:** gate sampling on initialized PTY roots (e831a41)
* **process:** keep validation detail internal (614a119)
* **process:** restrict cleanup to captured group leaders (40c6f60)
* **process:** settle exited zombie groups (072ce5a)
* **process:** settle exited zombie groups (4828326)
* **process:** stabilize and speed up the test suite (a3b7de9)
* **reference:** preserve distinct parse failures (e02cb2f)
* **reference:** preserve distinct parse failures (543510f)
* rollup batch of fixes (b348b2c)
* **runtime:** apply permission reloads atomically (49e843e)
* **runtime:** apply permission reloads atomically (3ae7109)
* **runtime:** serialize permission reloads (7e53dd6)
* **runtime:** unregister shutdown handlers (71072d8)
* **runtime:** unregister shutdown handlers (f9e3c23)
* **session:** isolate availability observers (43766fd)
* **session:** isolate availability observers (e5a80d4)
* **session:** reopen replaced targets (e98413c)
* **session:** reopen replaced targets (5c55999)
* **setup:** configure every detected client (69744a4)
* **setup:** configure every detected client (24f9a1f)
* **setup:** omit aligned client configurations from plan (a86da4f)
* **setup:** omit aligned skill from plan (d81687f)
* **setup:** omit aligned skill from plan (2984fa7)
* **setup:** preserve client config symlinks (85285f1)
* **setup:** preserve client config symlinks (df87544)
* **test:** adapt mainReload shutdown seam to registerShutdown signature (0a430c1)
* **tooling:** isolate concurrent repository checks (fb17156)
* **tooling:** isolate concurrent repository checks (ab8c5c1)
* **upgrade:** prevent version downgrades (a204840)
* **upgrade:** prevent version downgrades (1d1d234)
* **verify:** reconcile PR-212/215/228 package E2E expectations (cfa110c)


### Performance Improvements

* **application:** scan version artifacts in parallel (528c05e)
* **application:** scan version artifacts in parallel (c00739b)


### Tests

* **application:** verify packaged MCP replay (6601e0c)
* **browser:** harden Chrome startup on CI (74c5121)
* **browser:** route discovery sockets through proxy (e363f0e)
* **browser:** verify page-scoped Chrome transport (c252536)
* **cli:** verify packaged policy revocation (3d71737)
* **hopper:** cover verified Linux rejection (db202c2)
* **hopper:** retry after cancelled startup (6de726f)
* **hopper:** verify alternate Linux launcher path (d93257b)
* **package:** cover aligned setup plan (a597639)
* **package:** cover config symlink lifecycle (d1ef7a5)
* **package:** preserve unrelated symlink config (c50e51e)
* reduce test suite runtime (2223da1)
* **reference:** cover failure normalization (3d5041f)
* **runtime:** cover idempotent handler cleanup (1bdb59e)
* serialize subprocess-heavy integrations (f46fc7f)
* **session:** reopen replaced target through MCP (1c32880)
* **setup:** cover later clients after failure (8f73112)

## 1.5.0 (2026-07-14)


### Features

* add passive website reverse engineering (9986971)
* add passive website reverse engineering (2c1ceab)


### Bug Fixes

* **browser:** drop disallowed redirect evidence (8481be9)
* **browser:** scope CDP events and fail closed (5279d77)
* **browser:** scope workers and binary frame sizes (dfc06cf)
* harden PTY events and configured roots (ae8b1c5)
* harden PTY events and configured roots (31b40f3)
* **permission:** defer cache write grants (6a3fd5b)
* **permission:** defer cache write grants (f840e70)
* resolve triaged correctness issues (2575b30)
* resolve triaged correctness issues (e8ed307)
* resolve validation and artifact edge cases (2468682)
* resolve validation and artifact edge cases (ef7f2f9)


### Documentation

* add Hopper screenshot to README (a699fdd)
* add Hopper screenshot to README (08981a3)


### Tests

* **cli:** allow cold-start integration timing (7d5621d)

## 1.4.0 (2026-07-14)


### Features

* **core:** add typed policy and integrity contracts (190efca)
* **identity:** derive MCP surface metadata (2722722)
* **mcp:** expose progress resources and availability (da59299)
* **mcp:** land policy, resources, and typed contracts (8f79ee7)


### Bug Fixes

* **ci:** keep generated error docs with their owner (3e60e38)
* **ci:** preserve stacked integration changes (cf8e5cf)
* **cli:** return nonzero status for operation failures (#121) (00c187e)
* **cli:** return nonzero status for operation failures (#122) (964620a)
* **hopper:** complete owned Linux shutdown (#116) (fb51874)
* **mcp:** preserve migrated revisions and valid links (4149472)
* preserve actionable artifact diagnostics (#119) (7385220)
* **workspace:** migrate legacy integrity identities (d092d4c)


### Tests

* **identity:** defer live MCP integration proof (74db3fc)

## 1.3.0 (2026-07-13)


### Features

* add guided MCP workflow prompts (08d5b91)
* add guided MCP workflow prompts (24c3adb)
* add persistent cross-version investigation workspaces (c52eb46)
* add persistent cross-version investigation workspaces (41366ed)
* **analysis:** add provider-neutral persistent snapshots (c439b9e)
* **analysis:** persist snapshots and close Hopper reliably (c6407ef)
* **errors:** add caller-safe typed error projections (3be439c)
* **mcp:** return structured typed tool results (eb38e4c)


### Bug Fixes

* **bridge:** bound regex search work (733a382)
* **bridge:** bound regex search work (65682ee)
* **ci:** remove unused setup type export (c5728af)
* **cli:** render actionable analysis errors (af8c4ef)
* **copy:** use agent terminology (12060f6)
* **errors:** improve recovery guidance (77454dc)
* **errors:** return actionable caller-safe failures (fb0da03)
* **hopper:** cancel analysis and close documents reliably (179870e)
* **hopper:** return addresses for procedure relationships (2c707ab)
* **linux:** start Hopper demo sessions headlessly (32c5080)
* **linux:** start Hopper demo sessions headlessly (75818d1)
* **security:** restrict investigation artifact inputs (a2076b4)


### Tests

* **linux:** verify setup through CLI and MCP (67504d2)
* **package:** preserve unsupported host verification (977119f)
* strengthen MCP prompt acceptance coverage (05fb9b1)

## 1.2.0 (2026-07-13)


### Features

* **artifacts:** add approved native DMG traversal (24d000a)
* **process:** add deterministic capture v3 (d0e21f9)
* **process:** add deterministic capture v3 (5a361a6)
* **process:** introduce evidence-safe capture v4 (ee4d284)


### Bug Fixes

* **artifacts:** diagnose unpacked ASAR integrity failures (a504342)
* **ci:** remove redundant process exports (19bb231)
* **process:** harden capture validation and cleanup (ac78de0)


### Code Refactoring

* **artifacts:** simplify inventory traversal (c8d762e)
* **setup:** split setup and CLI registration (07e1b5a)


### Documentation

* document capture v4 and native mounts (aca518b)
* document process capture v3 (50f4a29)
* **process:** preserve capture invariants (841990b)
* **skill:** document capture v4 and DMG mounts (f0a9a3c)


### Tests

* **process:** use deterministic hang fixture (ba15d16)

## 1.1.0 (2026-07-13)


### Features

* **setup:** make installation explicit and safe (29d92ca)
* **setup:** make installation explicit and safe (3793889)


### Bug Fixes

* preserve requested evidence paths on macOS (0c0e2b8)
* preserve requested evidence paths on macOS (3d0ad79)


### Documentation

* **api:** regenerate TypeDoc reference (0a66cae)
* define HUREA contributor priorities (5df4ef6)
* explain the installation workflow (1c83263)

## 1.0.0 (2026-07-13)


### ⚠ BREAKING CHANGES

* **contracts:** batch_decompile, get_call_graph, and find_xrefs_to_name now return structured discriminated output shapes.

### Features

* **cli:** add self-upgrade command (c004220)
* **cli:** add self-upgrade command (0d77a9f)


### Bug Fixes

* **contracts:** keep error schema internal (ac8cc66)
* **contracts:** return structured workflow failures (4c54ff6)
* **native:** classify pre-aborted analysis first (dfd598f)


### Documentation

* list upgrade in CLI reference (8a24088)

## 0.5.0 (2026-07-13)


### Features

* **analysis:** harden agent workflows and evidence boundaries (883db91)
* **cli:** align terminal workflows with MCP (b1912b1)


### Bug Fixes

* **analysis:** accept valid final dossier pages (7c36f36)
* **bridge:** harden bounded Hopper boundaries (f8e8ea3)
* **cli:** preserve function provider provenance (c630f41)
* **lifecycle:** validate owned Hopper process identity (898d6b0)
* **process:** default capture networking to loopback (bce3398)
* **process:** keep network approval fail-closed (9526389)


### Code Refactoring

* **cli:** share direct analysis tool types (329fdf6)


### Documentation

* correct pull request tool inventory (d806480)
* document CLI safety and provider evaluation (efc9bd2)


### Tests

* **docs:** keep localized claims and tool counts aligned (a7b84a9)
* **verification:** strengthen conformance and real-Hopper checks (0d36976)

## 0.4.0 (2026-07-12)


### Features

* add cross-platform installation lifecycle (cc6a955)
* add cross-platform installation lifecycle (e651cb6)


### Documentation

* document installation and Linux support (034563a)
* simplify HUREA onboarding (e1dfe86)
* simplify HUREA onboarding (d85b661)


### Tests

* add package installation end-to-end coverage (993356b)
* stabilize artifact pagination coverage (f56bdde)


### Continuous Integration

* enforce conventional pull request titles (07a0b98)
* enforce conventional pull request titles (3a21f16)
* verify installed package with Linux Hopper (4f97f69)

## 0.3.0 (2026-07-12)


### Features

* add evidence-backed process investigations (cc8681a)
* **cli:** add guided local onboarding (8ca3db8)
* evolve HUREA analysis platform (4f18e26)
* **identity:** rename package and CLI to HUREA (3d70812)
* **mcp:** add typed bounded analysis tools (893d2e2)
* **session:** add dynamic binary lifecycle (f32e718)


### Bug Fixes

* **boundaries:** reject unsafe local inputs (15e8cf3)
* **doctor:** require an executable Hopper launcher (aee9cb8)
* **hopper:** launch analysis without stealing focus (ff321dc)
* **hopper:** make loader selection non-interactive (2b7ef86)
* keep execution options internal (167a824)
* **setup:** persist detected Hopper launcher (b2866e4)
* **setup:** preserve consent and startup target kind (a67054f)
* **setup:** preserve invalid MCP configuration (88f5edc)
* **targets:** cancel startup and probe PE offsets (66b8d6e)
* **verify:** tolerate exited Hopper helpers (b167bd7)


### Code Refactoring

* **cli:** share runtime between CLI and MCP (97541d8)


### Documentation

* document frictionless binary workflow (ee6d539)
* document the 43-tool workflow (1f235cb)
* record runtime and release constraints (62ede51)
* redesign and localize README (051b6db)
* redesign and localize README (910eda6)


### Tests

* add source-built Hopper conformance fixtures (d648bcd)

## 0.2.1 (2026-07-12)


### Documentation

* redesign and localize README (051b6db)
* redesign and localize README (910eda6)

## 0.2.0 (2026-07-12)


### Features

* **cli:** add guided local onboarding (8ca3db8)
* **identity:** rename package and CLI to HUREA (3d70812)
* **session:** add dynamic binary lifecycle (f32e718)


### Bug Fixes

* **boundaries:** reject unsafe local inputs (15e8cf3)
* **doctor:** require an executable Hopper launcher (aee9cb8)
* **hopper:** launch analysis without stealing focus (ff321dc)
* **hopper:** make loader selection non-interactive (2b7ef86)
* **setup:** persist detected Hopper launcher (b2866e4)
* **setup:** preserve consent and startup target kind (a67054f)
* **setup:** preserve invalid MCP configuration (88f5edc)
* **targets:** cancel startup and probe PE offsets (66b8d6e)
* **verify:** tolerate exited Hopper helpers (b167bd7)


### Code Refactoring

* **cli:** share runtime between CLI and MCP (97541d8)


### Documentation

* document frictionless binary workflow (ee6d539)
* record runtime and release constraints (62ede51)
