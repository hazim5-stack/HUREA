import { randomUUID } from "node:crypto";
import { tmpdir } from "node:os";
import { join } from "node:path";
import type { PermissionRequest } from "../domain/permissionPolicy.js";

/** Choose a fresh temporary destination for an artifact extraction. */
export const createArtifactExtractionDestination = (): string =>
  join(tmpdir(), `hurea-extracted-${randomUUID()}`);

/** Stable parent scope used to authorize HUREA-owned extraction destinations. */
export const artifactExtractionPermissionRoot = (): string => tmpdir();

/** Stable filesystem scope for the destination selected internally by HUREA. */
export const artifactExtractionPermissionRequest = (): PermissionRequest => ({
  capability: "artifact_extract",
  roots: [artifactExtractionPermissionRoot()],
  executables: [],
  environment_names: [],
  network: "none",
  mount: false,
  operation_identity: "extract_artifact:temporary_output",
});
