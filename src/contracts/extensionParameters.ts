import { z } from "zod";

const path = z.string().min(1).describe("Explicit local artifact file path");
const approval = z
  .boolean()
  .default(false)
  .describe("Explicit authority for this target and operation");
const duration = z
  .number()
  .positive()
  .max(10)
  .default(2)
  .describe("Finite observation window in seconds (maximum 10)");
const runtimeTarget = {
  pid: z.number().int().positive(),
  approved: approval,
  duration,
};

/** Mode-aware extension parameter schemas; provider boundaries validate remaining relationships. */
export const extensionParameterSchemas = {
  inspect_extension_providers: z.object({}).strict(),
  inspect_android_package: z
    .object({
      path,
      mode: z
        .enum(["inventory", "manifest", "decompile", "jni"])
        .default("inventory"),
    })
    .strict(),
  inspect_ios_package: z
    .object({ path, mode: z.enum(["bundle", "symbols"]).default("bundle") })
    .strict(),
  build_interprocedural_graph: z.object({ path }).strict(),
  trace_interprocedural_flow: z
    .object({
      path,
      source: z.string().min(1),
      direction: z.enum(["forward", "backward"]).default("forward"),
    })
    .strict(),
  compare_function_fingerprints: z
    .object({
      left: path,
      right: path,
      threshold: z.number().min(0).max(1).default(0.5),
    })
    .strict(),
  inspect_protocol_capture: z
    .object({
      path,
      format: z.enum(["har", "pcap", "protobuf"]).default("har"),
      compare: path.optional(),
    })
    .strict(),
  capture_protocol_session: z
    .object({
      interface: z.string().min(1),
      approved: approval,
      duration,
      filter: z.string().min(1).optional(),
    })
    .strict(),
  build_evidence_graph: z.object({ path }).strict(),
  inspect_firmware_image: z
    .object({
      path,
      mode: z.enum(["scan", "binwalk", "squashfs"]).default("scan"),
    })
    .strict(),
  inspect_external_binary: z
    .object({
      path,
      engine: z.enum(["lief", "rizin", "binaryninja", "ida"]).default("lief"),
      python: z.string().min(1).optional(),
      executable: z.string().min(1).optional(),
    })
    .strict(),
  manage_local_provider: z
    .object({
      path,
      mode: z.enum(["inspect", "register", "run"]).default("inspect"),
      approved: approval,
      registry: path.optional(),
      operation: z.string().min(1).optional(),
      target: path.optional(),
    })
    .strict(),
  observe_native_runtime: z
    .object({
      ...runtimeTarget,
      mode: z
        .enum(["modules", "threads", "trace", "memory", "jni", "objc", "swift"])
        .default("modules"),
      max_events: z.number().int().min(1).max(10000).default(1000),
      device_id: z.string().min(1).optional(),
      module: z.string().min(1).optional(),
      symbol: z.string().min(1).optional(),
      address: z.string().min(1).optional(),
      size: z.number().int().min(1).max(4096).default(256),
      class: z.string().min(1).optional(),
      selector: z.string().min(1).optional(),
      agent_path: path.optional(),
    })
    .strict(),
  observe_debugger_runtime: z
    .object({
      ...runtimeTarget,
      mode: z.enum(["snapshot", "trace"]).default("snapshot"),
      symbol: z.string().min(1).optional(),
    })
    .strict(),
};
