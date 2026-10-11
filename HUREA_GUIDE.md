# Getting started with HUREA

Developed and maintained by Hazim Batwa.

## Build and run

Use Node.js 22.19+ within the 22.x line, or Node.js 24.11+.
Python 3.10+ is required for extension operations.

```bash
git clone https://github.com/hazim5-stack/HUREA.git
cd HUREA
npm ci
npm run build:cached
npm link
hurea --help
hurea doctor
hurea setup
```

Setup previews configuration changes and requests approval before applying them.
For direct MCP use, configure the client to run `node` with the absolute path to
`scripts/hurea.mjs` followed by `mcp`. Keep the checkout at a stable location.

## Analysis providers

```bash
hurea providers --json
hurea extensions inspect_extension_providers -
```

Configure the providers needed for your investigation. Optional external tools
and their licenses are supplied separately.

See [installation](docs/installation.md), [extensions](docs/extensions.md), and
[README](README.md) for configuration and operation examples.

## License

Include [LICENSE](LICENSE) with all software distributions.
