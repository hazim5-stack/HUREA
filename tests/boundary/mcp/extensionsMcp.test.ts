import { Client, InMemoryTransport } from "@modelcontextprotocol/client";
import { McpServer } from "@modelcontextprotocol/server";
import { describe, expect, it } from "vitest";
import { registerExtensionTools } from "../../../src/server/registerExtensionTools.js";
import {
  EXTENSION_TOOL_CONTRACTS,
  extensionOutputSchema,
} from "../../../src/contracts/extensionToolContracts.js";
import { parseEvidence } from "../../../src/domain/evidence.js";

describe("optional extensions MCP transport", () => {
  it("lists the canonical inventory and returns valid Evidence and errors", async () => {
    const server = new McpServer({
      name: "hurea-extension-test",
      version: "1.0.0",
    });
    registerExtensionTools(server);
    const client = new Client({
      name: "hurea-extension-test",
      version: "1.0.0",
    });
    const [ct, st] = InMemoryTransport.createLinkedPair();
    try {
      await server.connect(st);
      await client.connect(ct);
      const tools = await client.listTools();
      expect(tools.tools.map((t) => t.name).sort()).toEqual(
        EXTENSION_TOOL_CONTRACTS.map((t) => t.name).sort(),
      );
      const status = await client.callTool({
        name: "inspect_extension_providers",
        arguments: { parameters: {} },
      });
      const value = extensionOutputSchema.parse(status.structuredContent);
      expect(value.ok).toBe(true);
      expect(
        value.evidence === undefined
          ? null
          : parseEvidence(value.evidence).operation,
      ).toBe("inspect_extension_providers");
      const denied = await client.callTool({
        name: "observe_debugger_runtime",
        arguments: { parameters: { pid: 1 } },
      });
      expect(denied.isError).toBe(true);
      expect(
        extensionOutputSchema.parse(denied.structuredContent).error?.code,
      ).toBe("AUTHORITY_REQUIRED");
    } finally {
      await client.close();
      await server.close();
    }
  });
});
