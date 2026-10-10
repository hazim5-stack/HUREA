import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

import { describe, expect, it } from "vitest";
import { SUPPORTED_CLIENT_DEFINITIONS } from "../../src/application/SupportedClients.js";
import { PRODUCT_IDENTITY } from "../../src/identity.js";

const readmes = [
  "REFERENCE.md",
  "README_zh.md",
  "README_ja.md",
  "README_ko.md",
  "README_ar.md",
] as const;

const normalizedProse = (content: string): string =>
  content.replace(/\s+/gu, " ").trim();

describe("localized README product facts", () => {
  it.each(readmes)(
    "keeps commands and requirements aligned in %s",
    async (path) => {
      const content = await readFile(resolve(path), "utf8");
      expect(content).toContain("bash ./install.sh");
      expect(content).toContain("npx hurea-agents setup");
      expect(content).toContain("npx --yes hurea-agents@latest setup");
      expect(content).toContain("npx -y hurea-agents@latest doctor");
      expect(content).toContain("hurea uninstall");
      expect(content).toContain(
        `"args": ["-y", "${PRODUCT_IDENTITY.registrationPackageSpecifier}", "mcp"]`,
      );
      expect(content).toContain("Node.js 22");
      expect(content).toContain("macOS 12");
      expect(content).toContain("Ubuntu 24.04");
      expect(content).toContain("Fedora 41");
      expect(content).toContain("Arch Linux");
      for (const client of SUPPORTED_CLIENT_DEFINITIONS)
        expect(content).toContain(client.displayName);
      if (path === "README_ar.md")
        expect(content).toContain("Windows غير مدعوم حاليًا");
      expect(content).toContain("MCP-tool_catalog");
    },
  );

  it("keeps both English CLI onboarding paths discoverable", async () => {
    const content = await readFile(resolve("REFERENCE.md"), "utf8");
    expect(content).toContain("npx -y hurea-agents@latest analyze");
    expect(content).toContain("npm install --global hurea-agents");
    expect(content).toContain("hurea setup");
    expect(content).toContain("--install-hopper");
    expect(content).toContain("docs/installation.md");
    expect(content).toContain("npx --yes hurea-agents@latest setup");
  });

  it("documents explicit setup freshness and rollback", async () => {
    const content = await readFile(resolve("docs/installation.md"), "utf8");
    const prose = normalizedProse(content);
    expect(prose).toContain(
      "npm exec --yes --package=hurea-agents@2.4.0 -- hurea setup",
    );
  });

  it("documents the published MCP Registry installation path", async () => {
    const content = await readFile(resolve("docs/installation.md"), "utf8");
    expect(content).toContain("MCP Registry");
    expect(content).toContain("local.hazim/hurea");
    expect(content).toContain('"command": "npx"');
    expect(content).toContain('"args": ["-y", "hurea-agents@latest", "mcp"]');
  });
});
