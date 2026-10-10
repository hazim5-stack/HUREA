import { CLI_COMMANDS } from "../cliCommandNames.js";
import { readFile } from "node:fs/promises";
import { z } from "incur";
import {
  extensionInputSchema,
  extensionOperationSchema,
} from "../contracts/extensionToolContracts.js";
import { runExtensionAnalysis } from "../application/ExtensionAnalysis.js";
import type { CliInstance } from "./types.js";

/** Expose every optional extension workflow with the same parameters as MCP. */
export const registerExtensionCommands = (cli: CliInstance): void => {
  cli.command(CLI_COMMANDS.extensions, {
    description:
      "Run an extension operation with a local JSON parameters file; see docs/extensions.md",
    args: z.object({
      operation: extensionOperationSchema.describe(
        "Canonical extension operation name",
      ),
      request: z
        .string()
        .describe("JSON parameters file; use - for an empty object"),
    }),
    run: async ({ args }) => {
      try {
        const text =
          args.request === "-" ? "{}" : await readFile(args.request, "utf8");
        if (Buffer.byteLength(text) > 16 * 1024 * 1024)
          return {
            ok: false,
            error: {
              code: "RESOURCE_LIMIT",
              message: "Request exceeds 16 MiB",
            },
          };
        const parameters = extensionInputSchema.parse({
          parameters: JSON.parse(text),
        }).parameters;
        return await runExtensionAnalysis(args.operation, parameters);
      } catch (error: unknown) {
        return {
          ok: false,
          error: {
            code: "INVALID_INPUT",
            message: error instanceof Error ? error.message : "Invalid request",
          },
        };
      }
    },
  });
};
