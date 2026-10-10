# HUREA rebrand

- Full name: Hazim Universal Reverse Engineering for Anything.
- CLI: `hurea`; npm package identity: `hurea-agents` (local, unpublished).
- MCP configuration key: `hurea`; local manifest identity: `local.hazim/hurea` (not a registered public namespace).
- Environment variable prefix: `HUREA_`; configuration file: `hurea.json`.
- Bundled routing skill: `hurea-reverse-engineering`.
- Java/Swift bridge filenames and class names use Hurea.
- The upstream version 3.2.1 is retained to identify the source snapshot.

## Local installation

Use Node.js 22.19+ or 24.11+. From this folder:

```bash
npm ci
npm run build:cached
npm link
hurea --help
hurea setup
hurea doctor
```

Setup is interactive and writes client registrations only after showing its plan.
For direct MCP use, configure your client to run the absolute path to `scripts/hurea.mjs` with argument `mcp`. This executable has a Node shebang. Keep this directory at a stable location.

## Existing installations

This fork uses independent names and does not migrate existing REA settings automatically. Configure HUREA separately. Public npm and MCP Registry examples inherited in the guides are future publication templates. No HUREA package, repository, registry entry, or release has been published by this task.

`private: true` protects against accidental publication. Select your own repository and a verified registry namespace before enabling publishing. Upstream links in history and attribution identify the original developer, not this fork's release channel.

## Attribution

About and README footers render the original developer in `<small>` text. LICENSE is plain text and preserves the complete original MIT notice; attribution there cannot have a visual font size. See ABOUT.md, NOTICE.md and LICENSE.

This change updates branding, not the analysis capabilities. Frida, JADX, LLDB and other previously proposed features have not been added.

## Verification in this environment

- TypeScript build succeeded.
- `npm run check:fast` succeeded (typecheck and lint; 74 warnings, no errors).
- 60 focused tests passed in 8 files: setup planning/configuration, routing skill installation, local installer, README/release metadata, and MCP server boundary.
- `hurea about` and CLI help executed with HUREA identity.
- Package metadata, MCP tool catalog, skill metadata, product catalog and documentation facts checks passed.
- Real Hopper, Ghidra, macOS Swift UI bridge, and Windows provider execution were not exercised.
