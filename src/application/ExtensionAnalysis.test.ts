import { afterEach, describe, expect, it } from "vitest";
import { mkdtemp, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { runExtensionAnalysis } from "../application/ExtensionAnalysis.js";
import { parseEvidence } from "../domain/evidence.js";
import { executeExtension } from "../extensions/ExtensionBridge.js";

const temporary: string[] = [];
afterEach(async () => {
  await Promise.all(
    temporary.splice(0).map((p) => rm(p, { recursive: true, force: true })),
  );
});
describe("extension bridge real local execution", () => {
  it("returns canonical verifiable Evidence", async () => {
    const r = await runExtensionAnalysis("inspect_extension_providers", {});
    expect(r.ok).toBe(true);
    if (r.evidence !== undefined)
      expect(parseEvidence(r.evidence).operation).toBe(
        "inspect_extension_providers",
      );
    else throw new Error("Missing Evidence");
  });
  it("binds graph evidence to an immutable input digest", async () => {
    const dir = await mkdtemp(join(tmpdir(), "hurea-ext-test-"));
    temporary.push(dir);
    const path = join(dir, "flow.json");
    await writeFile(
      path,
      JSON.stringify({
        nodes: [{ id: "a" }, { id: "b" }],
        edges: [{ from: "a", to: "b" }],
      }),
    );
    const r = await runExtensionAnalysis("trace_interprocedural_flow", {
      path,
      source: "a",
    });
    expect(r.evidence?.confidence).toBe("derived");
    expect(r.evidence?.subject?.digest.sha256).toMatch(/^[a-f0-9]{64}$/u);
    expect(
      r.evidence === undefined ? null : parseEvidence(r.evidence).operation,
    ).toBe("trace_interprocedural_flow");
  });
  it("projects authority failures instead of attaching", async () => {
    const r = await runExtensionAnalysis("observe_native_runtime", { pid: 1 });
    expect(r.error?.code).toBe("AUTHORITY_REQUIRED");
  });
  it("rejects unknown operation", async () => {
    expect((await runExtensionAnalysis("made_up", {})).error?.code).toBe(
      "INVALID_INPUT",
    );
  });
  it("honors pre-cancellation", async () => {
    expect(
      (
        await executeExtension(
          "inspect_extension_providers",
          {},
          AbortSignal.abort(),
        )
      ).ok,
    ).toBe(false);
  });
  it("cancels an active child provider", async () => {
    const dir = await mkdtemp(join(tmpdir(), "hurea-ext-cancel-"));
    temporary.push(dir);
    const target = join(dir, "target");
    await writeFile(target, "x");
    const manifest = join(dir, "manifest.json");
    await writeFile(
      manifest,
      JSON.stringify({
        schema_version: 1,
        id: "slow",
        executable: "python3",
        operations: {
          wait: {
            args: ["-c", "import time;time.sleep(30)", "{target}"],
            mutates_target: false,
            writes_filesystem: false,
            accesses_network: false,
          },
        },
      }),
    );
    const c = new AbortController();
    const timer = setTimeout(() => c.abort(), 300);
    const r = await executeExtension(
      "manage_local_provider",
      {
        path: manifest,
        target,
        mode: "run",
        approved: true,
        operation: "wait",
      },
      c.signal,
    );
    clearTimeout(timer);
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.error.code).toBe("CANCELLED");
  });
});
