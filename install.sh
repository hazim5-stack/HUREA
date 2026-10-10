#!/bin/bash
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
start_setup=true
dry_run=false
while (($#)); do
  case "$1" in
    --no-setup|--no-prompt) start_setup=false ;;
    --dry-run) dry_run=true ;;
    --help|-h) printf 'HUREA local installer: install.sh [--dry-run] [--no-setup]\n'; exit 0 ;;
    *) printf 'Unknown option: %s\n' "$1" >&2; exit 1 ;;
  esac
  shift
done
printf 'HUREA local install plan\n  Source: %s\n  Install locked dependencies, build, and link hurea.\n' "$script_dir"
if [[ "$dry_run" == true ]]; then exit 0; fi
command -v node >/dev/null || { printf 'Node.js 22.19+ or 24.11+ is required.\n' >&2; exit 1; }
command -v npm >/dev/null || { printf 'npm is required.\n' >&2; exit 1; }
cd "$script_dir"
npm ci
npm run build:cached
npm link
if [[ "$start_setup" == true ]]; then node scripts/hurea.mjs setup; fi
