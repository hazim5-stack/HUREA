import { toolContractMetadata } from "./toolEffects.js";
import { extensionParameterSchemas } from "./extensionParameters.js";
import { z } from "zod";
import { evidenceSchema } from "../domain/evidence.js";
import { jsonValueSchema } from "../domain/jsonValue.js";
import type { ToolContract } from "./toolContractTypes.js";

const descriptions = {
  capture_protocol_session:
    "Capture metadata on an explicitly approved local interface with tshark. Parameters: interface, approved=true, duration<=10, filter? (BPF). Bounded to 10,000 packets; raw temporary capture deleted. No TLS interception or injection.",
  build_interprocedural_graph:
    "Build a context-insensitive def-use/argument/return graph from explicit SSA JSON IR. Parameters: path. IR: {functions:[{id,parameters:[variable],instructions:[{id,kind,defs?,uses?,callee?,args?}]}]}. Returns unresolved definitions/calls separately; no automatic alias inference.",
  inspect_extension_providers:
    "Report bring-your-own executable and Python module availability. Parameters: {}. Presence does not prove tool compatibility or licensing.",
  inspect_android_package:
    "Inspect an APK. Parameters: path, mode=inventory|manifest|decompile|jni. Manifest requires aapt2; decompile/JNI require JADX; JNI exports require nm. Reports native declarations separately from JNI exports, without asserting resolved bridges.",
  inspect_ios_package:
    "Inspect an IPA's plists, profiles, source storyboard/XIB elements and UI asset paths. Parameters: path, mode=bundle|symbols. Profiles require OpenSSL; symbols require Mach-O capable nm. No encrypted executable or SwiftUI reconstruction.",
  trace_interprocedural_flow:
    "Traverse explicit def-use, argument, return or field edges across an imported JSON graph {nodes:[{id}],edges:[{from,to}]}. Parameters: path, source, direction=forward|backward. Does not invent alias or path feasibility facts.",
  compare_function_fingerprints:
    "Compare imported JSON {functions:[{id,instructions?,strings?,constants?,calls?,cfg_edges?}]} records. Parameters: left, right, threshold=0.5. Greedy heuristic Jaccard matching; score is not a confidence probability; splits/merges unresolved.",
  inspect_protocol_capture:
    "Inspect a local HAR and infer sample JSON schemas. Parameters: path, compare? (second HAR). Reports endpoints/status/header names and redacts header/query/scalar values. format=har|pcap|protobuf. PCAP needs tshark; descriptor-free protobuf tag inspection needs protoc. No complete protobuf/API reconstruction.",
  build_evidence_graph:
    "Build an offline interactive SVG Evidence graph and HTML viewer as an inline result. Parameters: path (JSON array of Evidence or {evidence:[]}). Does not write files; caller can save result.html. Imported records are not automatically trusted.",
  inspect_firmware_image:
    "Scan firmware signature offsets or use bring-your-own binwalk/unsquashfs listing. Parameters: path, mode=scan|binwalk|squashfs. Magic hits remain inferred candidates; does not execute or extract embedded firmware.",
  inspect_external_binary:
    "Analyze a binary using LIEF, Rizin, Binary Ninja or IDA/optional Hex-Rays. Parameters: path, engine=lief|rizin|binaryninja|ida, python? (Binary Ninja environment), executable? (IDA). IDA runs on a temporary copy; no license is installed.",
  manage_local_provider:
    "Inspect/register/run a trusted local provider SDK manifest. Parameters: path (manifest), mode=inspect|register|run, approved (required register/run), registry (register), operation/target (run). Manifests declare exact argv and effects; no remote install or sandbox enforcement. Registry writes are atomic with backup.",
  observe_native_runtime:
    "Attach Frida for a bounded native observation. Parameters: pid, approved=true, mode=modules|threads|trace|memory|jni|objc|swift, duration<=10, max_events<=10000, device_id?, module/symbol or address (trace/swift), address/size<=4096 (memory), class/selector (objc), agent_path? (explicit trusted compiled bridge). Finally unloads and detaches. Hooks affect timing/code pages; ABI values remain unresolved. ObjC modern Frida requires a compiled bridge agent.",
  observe_debugger_runtime:
    "Attach LLDB for a bounded snapshot or symbol breakpoint trace, then detach. Parameters: pid, approved=true, mode=snapshot|trace, symbol (trace), duration<=10. Temporarily stops target; no target launch. Requires host attach permissions.",
} as const;

/** Extension operation names shared by the CLI, MCP and bridge. */
export const extensionOperationSchema = z.enum([
  "capture_protocol_session",
  "build_interprocedural_graph",
  "inspect_extension_providers",
  "inspect_android_package",
  "inspect_ios_package",
  "trace_interprocedural_flow",
  "compare_function_fingerprints",
  "inspect_protocol_capture",
  "build_evidence_graph",
  "inspect_firmware_image",
  "inspect_external_binary",
  "manage_local_provider",
  "observe_native_runtime",
  "observe_debugger_runtime",
]);
/** Validated caller parameters; operation-specific semantics are enforced by the bridge. */
export const extensionInputSchema = z.object({
  parameters: z.record(z.string(), jsonValueSchema).default({}),
});
/** Every extension returns canonical Evidence or an actionable tagged error. */
export const extensionOutputSchema = z.object({
  ok: z.boolean(),
  evidence: evidenceSchema.optional(),
  error: z.object({ code: z.string(), message: z.string() }).optional(),
});

/** Public extension inventory and conservative effects for mode-dependent tools. */
export const EXTENSION_TOOL_CONTRACTS = Object.entries(descriptions).map(
  ([name, description]) => {
    const exampleParameters =
      name === "inspect_extension_providers"
        ? {}
        : name === "capture_protocol_session"
          ? { interface: "lo", approved: false }
          : name.startsWith("observe_")
            ? { pid: 1234, approved: false }
            : name === "compare_function_fingerprints"
              ? { left: "/tmp/left.json", right: "/tmp/right.json" }
              : name === "trace_interprocedural_flow"
                ? { path: "/tmp/flow.json", source: "input" }
                : { path: "/tmp/artifact" };
    return {
      name,
      ...toolContractMetadata(name),
      description,
      kind: "application",
      inputSchema: z.object({
        parameters:
          extensionParameterSchemas[extensionOperationSchema.parse(name)],
      }),
      outputSchema: extensionOutputSchema,
      examples: [
        {
          title: "Example explicit local target parameters",
          input: { parameters: exampleParameters },
        },
      ],
    } satisfies ToolContract;
  },
);
