import type { McpServer } from "@modelcontextprotocol/server";
import type { BinarySessionPort } from "../application/BinarySession.js";
import { runExtensionAnalysis } from "../application/ExtensionAnalysis.js";
import {
  extensionInputSchema,
  EXTENSION_TOOL_CONTRACTS,
} from "../contracts/extensionToolContracts.js";
import { toolRegistrationOptions } from "./toolRegistrationOptions.js";

/** Register optional extension tools and retain their Evidence in the active session. */
export const registerExtensionTools = (
  server: McpServer,
  session?: BinarySessionPort,
): void => {
  for (const contract of EXTENSION_TOOL_CONTRACTS) {
    server.registerTool(
      contract.name,
      toolRegistrationOptions(contract),
      async (input, context) => {
        const result = await runExtensionAnalysis(
          contract.name,
          extensionInputSchema.parse(input).parameters,
          context.mcpReq.signal,
        );
        if (
          result.ok &&
          result.evidence !== undefined &&
          session !== undefined
        ) {
          const recorded = session.recordEvidence(result.evidence);
          if (!recorded.ok)
            return {
              isError: true,
              content: [
                {
                  type: "text",
                  text: "Could not retain extension Evidence in the session",
                },
              ],
            };
        }
        return {
          isError: !result.ok,
          structuredContent: result,
          content: [{ type: "text", text: JSON.stringify(result) }],
        };
      },
    );
  }
};
