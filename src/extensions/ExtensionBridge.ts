import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { z } from "zod";
import { jsonValueSchema, type JsonValue } from "../domain/jsonValue.js";

const bridgeOutputSchema = z.discriminatedUnion("ok", [
  z.object({
    ok: z.literal(true),
    result: z.object({
      data: jsonValueSchema,
      confidence: z.enum(["observed", "derived", "inferred"]),
      limitations: z.array(z.string()),
      subject: z
        .object({
          path: z.string(),
          sha256: z.string().regex(/^[a-f0-9]{64}$/u),
        })
        .nullable(),
    }),
  }),
  z.object({
    ok: z.literal(false),
    error: z.object({ code: z.string(), message: z.string() }),
  }),
]);

/** Execute one bounded local bridge request without shell expansion or target launch. */
export const executeExtension = async (
  operation: string,
  parameters: Readonly<Record<string, JsonValue>>,
  signal?: AbortSignal,
): Promise<z.infer<typeof bridgeOutputSchema>> => {
  const error = validateRequest(operation, parameters, signal);
  if (error !== undefined) return error;
  const request = JSON.stringify({ operation, parameters });
  return new Promise((resolve) => {
    const bridge = fileURLToPath(
      new URL("../../bridge/extensions/engine.py", import.meta.url),
    );
    const child = spawn(
      process.env.HUREA_EXTENSION_PYTHON ?? "python3",
      [bridge],
      {
        env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
        stdio: ["pipe", "pipe", "pipe"],
        detached: process.platform !== "win32",
      },
    );
    let output = "",
      stderr = "",
      bytes = 0,
      reason: string | undefined;
    let forceTimer: ReturnType<typeof setTimeout> | undefined;
    const terminate = (why: string): void => {
      if (reason !== undefined) return;
      reason = why;
      const kill = (sig: NodeJS.Signals): void => {
        try {
          if (process.platform !== "win32" && child.pid !== undefined)
            process.kill(-child.pid, sig);
          else child.kill(sig);
        } catch {
          /* Already exited. */
        }
      };
      kill("SIGTERM");
      forceTimer = setTimeout(() => kill("SIGKILL"), 2000);
      forceTimer.unref();
    };
    const cancel = (): void => terminate("CANCELLED");
    signal?.addEventListener("abort", cancel, { once: true });
    if (signal?.aborted) cancel();
    const timer = setTimeout(() => terminate("TIMEOUT"), 60000);
    timer.unref();
    const cleanup = (): void => {
      clearTimeout(timer);
      if (forceTimer !== undefined) clearTimeout(forceTimer);
      signal?.removeEventListener("abort", cancel);
    };
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk: string) => {
      bytes += Buffer.byteLength(chunk);
      if (bytes > 16 * 1024 * 1024) terminate("RESOURCE_LIMIT");
      else output += chunk;
    });
    child.stderr.on("data", (chunk: string) => {
      if (stderr.length < 4096) stderr += chunk.slice(0, 4096 - stderr.length);
    });
    child.stdin.on("error", () => {
      /* Spawn or early provider exit is projected below. */
    });
    child.on("error", (error) => {
      cleanup();
      resolve({
        ok: false,
        error: { code: "DEPENDENCY_MISSING", message: error.message },
      });
    });
    child.on("close", (code) => {
      cleanup();
      if (reason !== undefined || code !== 0) {
        resolve({
          ok: false,
          error: {
            code: reason ?? "PROVIDER_FAILED",
            message: `Extension bridge ${reason ?? `exit ${code}`}: ${stderr}`,
          },
        });
        return;
      }
      try {
        resolve(bridgeOutputSchema.parse(JSON.parse(output)));
      } catch {
        resolve({
          ok: false,
          error: {
            code: "INVALID_PROVIDER_OUTPUT",
            message: "Expected one validated bridge JSON response",
          },
        });
      }
    });
    child.stdin.end(request);
  });
};

const validateRequest = (
  operation: string,
  parameters: Readonly<Record<string, JsonValue>>,
  signal?: AbortSignal,
): z.infer<typeof bridgeOutputSchema> | undefined => {
  if (signal?.aborted)
    return {
      ok: false,
      error: { code: "CANCELLED", message: "Extension request cancelled" },
    };
  if (
    Buffer.byteLength(JSON.stringify({ operation, parameters })) >
    16 * 1024 * 1024
  )
    return {
      ok: false,
      error: { code: "RESOURCE_LIMIT", message: "Request exceeds 16 MiB" },
    };
  return undefined;
};
