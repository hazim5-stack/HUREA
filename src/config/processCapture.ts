import type {
  EnabledProcessExecutionPolicy,
  ProcessExecutionPolicy,
} from "../domain/processCapture.js";
import { ConfigurationError } from "../domain/errors.js";
import type { PermissionCeiling } from "../domain/permissionPolicy.js";
import { err, ok, type Result } from "../domain/result.js";
import type { Environment } from "./environment.js";
import { parseAbsoluteRoots, parseStringArray } from "./parsers.js";
import { permissionScope } from "./permissions.js";

/** Parse process capture into disabled or fully authorized state. */
export const parseProcessExecutionPolicy = (
  env: Environment,
): Result<ProcessExecutionPolicy, ConfigurationError> => {
  const executableRoots = parseAbsoluteRoots(
    env.HUREA_PROCESS_EXECUTABLE_ROOTS_JSON,
    "HUREA_PROCESS_EXECUTABLE_ROOTS_JSON",
  );
  if (!executableRoots.ok) return executableRoots;
  const workingRoots = parseAbsoluteRoots(
    env.HUREA_PROCESS_WORKING_ROOTS_JSON,
    "HUREA_PROCESS_WORKING_ROOTS_JSON",
  );
  if (!workingRoots.ok) return workingRoots;
  const allowedEnvironment = parseStringArray(
    env.HUREA_PROCESS_ALLOWED_ENV_JSON,
    "HUREA_PROCESS_ALLOWED_ENV_JSON",
  );
  if (!allowedEnvironment.ok) return allowedEnvironment;
  if (env.HUREA_PROCESS_CAPTURE_ENABLED !== "true")
    return ok({ status: "disabled" });
  const parsedExecutables = requireRoots(
    executableRoots.value,
    "HUREA_PROCESS_EXECUTABLE_ROOTS_JSON must encode at least one absolute root when process capture is enabled",
  );
  if (!parsedExecutables.ok) return parsedExecutables;
  const parsedWorking = requireRoots(
    workingRoots.value,
    "HUREA_PROCESS_WORKING_ROOTS_JSON must encode at least one absolute root when process capture is enabled",
  );
  if (!parsedWorking.ok) return parsedWorking;
  return ok({
    status: "enabled",
    executableRoots: parsedExecutables.value,
    workingRoots: parsedWorking.value,
    allowedEnvironment: allowedEnvironment.value,
    networkAccess:
      env.HUREA_PROCESS_ALLOW_EXTERNAL_NETWORK === "true" ? "external" : "none",
  });
};

/** Add the exact process-capture ceiling when capture is enabled. */
export const appendProcessCaptureCeiling = (
  ceilings: PermissionCeiling[],
  policy: ProcessExecutionPolicy,
): void => {
  if (policy.status === "disabled") return;
  ceilings.push(
    permissionScope("process_capture", policy.workingRoots, {
      executables: policy.executableRoots,
      environment_names: policy.allowedEnvironment,
      network: policy.networkAccess,
    }),
  );
};

const requireRoots = (
  roots: readonly string[],
  message: string,
): Result<
  EnabledProcessExecutionPolicy["workingRoots"],
  ConfigurationError
> => {
  const [first, ...remaining] = roots;
  return first === undefined
    ? err(new ConfigurationError(message))
    : ok([first, ...remaining]);
};
