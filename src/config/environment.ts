import { z } from "zod";
import { isAbsolute } from "node:path";

import { ConfigurationError } from "../domain/errors.js";
import { err, ok, type Result } from "../domain/result.js";
import { analysisProviderSelectorSchema } from "../contracts/providerSelection.js";

const environmentSchema = z
  .object({
    HUREA_ANALYSIS_PROVIDER: analysisProviderSelectorSchema.default("auto"),
    GHIDRA_INSTALL_DIR: z
      .string()
      .min(1)
      .refine(isAbsolute, "GHIDRA_INSTALL_DIR must be absolute")
      .optional(),
    JAVA_HOME: z
      .string()
      .min(1)
      .refine(isAbsolute, "JAVA_HOME must be absolute")
      .optional(),
    HUREA_ILSPY_CMD_PATH: z
      .string()
      .min(1)
      .refine(isAbsolute, "HUREA_ILSPY_CMD_PATH must be absolute")
      .optional(),
    HOPPER_LAUNCHER_PATH: z.string().min(1).optional(),
    HOPPER_TARGET_PATH: z.string().min(1).optional(),
    HOPPER_TARGET_KIND: z
      .enum(["executable", "database"])
      .default("executable"),
    HOPPER_LOADER_ARGS_JSON: z.string().optional(),
    HUREA_LOG_LEVEL: z
      .enum(["trace", "debug", "info", "warn", "error", "fatal", "silent"])
      .default("info"),
    HUREA_PROCESS_CAPTURE_ENABLED: z.enum(["true", "false"]).default("false"),
    HUREA_PROCESS_CAPTURE_AUTO_GRANT: z.enum(["true", "false"]).default("true"),
    HUREA_ARTIFACT_NATIVE_MOUNT_ENABLED: z
      .enum(["true", "false"])
      .default("false"),
    HUREA_ARTIFACT_INTEGRITY_CONTINUE_ENABLED: z
      .enum(["true", "false"])
      .default("false"),
    HUREA_PROCESS_ALLOW_EXTERNAL_NETWORK: z
      .enum(["true", "false"])
      .default("false"),
    HUREA_PROCESS_EXECUTABLE_ROOTS_JSON: z.string().default("[]"),
    HUREA_PROCESS_WORKING_ROOTS_JSON: z.string().default("[]"),
    HUREA_PROCESS_ALLOWED_ENV_JSON: z.string().default("[]"),
    HUREA_REFERENCE_SECRET_PATTERNS_JSON: z.string().default("[]"),
    HUREA_BROWSER_OBSERVE_ENABLED: z.enum(["true", "false"]).default("false"),
    HUREA_BROWSER_CDP_ENDPOINTS_JSON: z.string().default("[]"),
    HUREA_BROWSER_ALLOWED_ORIGINS_JSON: z.string().default("[]"),
    HUREA_BROWSER_SCENARIO_ENABLED: z.enum(["true", "false"]).default("false"),
    HUREA_BROWSER_SCENARIO_AUTO_GRANT: z
      .enum(["true", "false"])
      .default("false"),
    HUREA_BROWSER_SCENARIO_EXECUTABLE_ROOTS_JSON: z.string().default("[]"),
    HUREA_BROWSER_SCENARIO_CDP_ENDPOINTS_JSON: z.string().default("[]"),
    HUREA_BROWSER_SCENARIO_ALLOWED_ORIGINS_JSON: z.string().default("[]"),
    HUREA_BROWSER_SCENARIO_ALLOWED_ENV_JSON: z.string().default("[]"),
    HUREA_ELECTRON_OBSERVE_ENABLED: z.enum(["true", "false"]).default("false"),
    HUREA_ELECTRON_AUTOMATE_ENABLED: z.enum(["true", "false"]).default("false"),
    HUREA_ELECTRON_AUTOMATE_AUTO_GRANT: z
      .enum(["true", "false"])
      .default("false"),
    HUREA_ELECTRON_AUTOMATE_EXECUTABLE_ROOTS_JSON: z.string().default("[]"),
    HUREA_ELECTRON_AUTOMATE_APPLICATION_ROOTS_JSON: z.string().default("[]"),
    HUREA_V8_INSPECTOR_OBSERVE_ENABLED: z
      .enum(["true", "false"])
      .default("false"),
    HUREA_JAVASCRIPT_REPLAY_ENABLED: z.enum(["true", "false"]).default("false"),
    HUREA_JAVASCRIPT_REPLAY_ROOTS_JSON: z.string().default("[]"),
    HUREA_JAVASCRIPT_REPLAY_NODE_PATH: z
      .string()
      .min(1)
      .refine(isAbsolute, "HUREA_JAVASCRIPT_REPLAY_NODE_PATH must be absolute")
      .default(process.execPath),
    HUREA_JAVASCRIPT_REPLAY_BWRAP_PATH: z
      .string()
      .min(1)
      .refine(isAbsolute, "HUREA_JAVASCRIPT_REPLAY_BWRAP_PATH must be absolute")
      .default("/usr/bin/bwrap"),
    HUREA_JAVASCRIPT_REPLAY_SYSTEMD_RUN_PATH: z
      .string()
      .min(1)
      .refine(
        isAbsolute,
        "HUREA_JAVASCRIPT_REPLAY_SYSTEMD_RUN_PATH must be absolute",
      )
      .default("/usr/bin/systemd-run"),
    HUREA_JAVASCRIPT_REPLAY_SYSTEMCTL_PATH: z
      .string()
      .min(1)
      .refine(
        isAbsolute,
        "HUREA_JAVASCRIPT_REPLAY_SYSTEMCTL_PATH must be absolute",
      )
      .default("/usr/bin/systemctl"),
    HUREA_JAVASCRIPT_REPLAY_SHELL_PATH: z
      .string()
      .min(1)
      .refine(isAbsolute, "HUREA_JAVASCRIPT_REPLAY_SHELL_PATH must be absolute")
      .default("/usr/bin/bash"),
    HUREA_MANAGED_RUNTIME_ENABLED: z.enum(["true", "false"]).default("false"),
    HUREA_MANAGED_RUNTIME_ROOTS_JSON: z.string().default("[]"),
    HUREA_MANAGED_RUNTIME_EXECUTABLE_PATH: z
      .string()
      .min(1)
      .refine(
        isAbsolute,
        "HUREA_MANAGED_RUNTIME_EXECUTABLE_PATH must be absolute",
      )
      .default("/usr/bin/dotnet"),
    HUREA_PERMISSION_PROJECT_ROOT: z.string().min(1).optional(),
    HUREA_PERMISSION_PROJECT_STORE: z.string().min(1).optional(),
  })
  .refine(
    (value) =>
      (value.HUREA_PERMISSION_PROJECT_ROOT === undefined) ===
      (value.HUREA_PERMISSION_PROJECT_STORE === undefined),
    {
      message:
        "HUREA_PERMISSION_PROJECT_ROOT and HUREA_PERMISSION_PROJECT_STORE must be configured together",
    },
  );

export type Environment = z.infer<typeof environmentSchema>;

export const parseEnvironment = (
  environment: Readonly<Record<string, string | undefined>>,
): Result<Environment, ConfigurationError> => {
  const parsed = environmentSchema.safeParse(environment);
  if (!parsed.success) {
    return err(
      new ConfigurationError("Invalid HUREA environment configuration", {
        cause: parsed.error,
      }),
    );
  }
  return ok(parsed.data);
};
