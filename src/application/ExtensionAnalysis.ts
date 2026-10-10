import { extensionParameterSchemas } from "../contracts/extensionParameters.js";
import { z } from "zod";
import { jsonValueSchema } from "../domain/jsonValue.js";
import { createEvidence } from "../domain/evidence.js";
import type { JsonValue } from "../domain/jsonValue.js";
import {
  extensionOperationSchema,
  extensionOutputSchema,
} from "../contracts/extensionToolContracts.js";
import { executeExtension } from "../extensions/ExtensionBridge.js";

/** Shared CLI/MCP extension workflow, preserving canonical Evidence semantics. */
export const runExtensionAnalysis = async (
  operation: string,
  parameters: Readonly<Record<string, JsonValue>>,
  signal?: AbortSignal,
): Promise<z.infer<typeof extensionOutputSchema>> => {
  const checked = extensionOperationSchema.safeParse(operation);
  if (!checked.success)
    return {
      ok: false,
      error: { code: "INVALID_INPUT", message: "Unknown extension operation" },
    };
  const parsed = extensionParameterSchemas[checked.data].safeParse(parameters);
  if (!parsed.success)
    return {
      ok: false,
      error: { code: "INVALID_INPUT", message: parsed.error.message },
    };
  const validated = z.record(z.string(), jsonValueSchema).parse(parsed.data);
  const response = await executeExtension(checked.data, validated, signal);
  if (!response.ok) return response;
  const { subject, data, confidence, limitations } = response.result;
  const evidence = createEvidence(
    subject === null ? undefined : { ...subject, format: "file" },
    { id: "hurea-extensions", name: "HUREA Extensions", version: "1.0.0" },
    {
      operation,
      parameters: validated,
      result: data,
      confidence,
      authority:
        confidence === "observed" ? "shipped-artifact" : "analyst-inference",
      limitations,
    },
  );
  return extensionOutputSchema.parse({ ok: true, evidence });
};
