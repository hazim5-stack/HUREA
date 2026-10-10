import {
  createAnalysisProfile,
  type AnalysisProfileCommitment,
} from "../domain/analysisProfile.js";

/** Provider identity for deterministic composed analysis workflows. */
export const HUREA_WORKFLOW_PROVIDER = {
  id: "hurea-workflow",
  name: "HUREA composed investigation workflow",
  version: "1",
} as const;

/** Commit a workflow result to the exact upstream deep-analysis profile. */
export const workflowAnalysisProfile = (
  upstream: AnalysisProfileCommitment,
): AnalysisProfileCommitment =>
  createAnalysisProfile(HUREA_WORKFLOW_PROVIDER, {
    upstream_analysis_profile: upstream,
  });

/** Provider identity for deterministic artifact inventories. */
export const ARTIFACT_GRAPH_PROVIDER = {
  id: "hurea-artifact-graph",
  name: "HUREA safe artifact graph provider",
  version: "1",
} as const;

/** Provider identity for execution-free managed PE/CLI analysis. */
export const MANAGED_STATIC_PROVIDER = {
  id: "hurea-dotnet-static",
  name: "HUREA managed static analysis provider",
  version: "1",
} as const;

/** Provider identity for deterministic managed-code comparison workflows. */
export const MANAGED_WORKFLOW_PROVIDER = {
  id: "hurea-dotnet-workflows",
  name: "HUREA managed-code workflows",
  version: "1",
} as const;

/** Provider identity for deterministic Apple application projections. */
export const APPLE_APPLICATION_PROVIDER = {
  id: "hurea-apple-application",
  name: "HUREA Apple application workflows",
  version: "1",
} as const;

/** Provider identity for deterministic Android application projections. */
export const ANDROID_APPLICATION_PROVIDER = {
  id: "hurea-android-application",
  name: "HUREA Android application workflows",
  version: "1",
} as const;

/** Provider identity for deterministic static JavaScript application analysis. */
export const JAVASCRIPT_APPLICATION_PROVIDER = {
  id: "hurea-javascript-application",
  name: "HUREA JavaScript application analyzer",
  version: "1",
} as const;

/** Provider identity for static/passive-runtime JavaScript reconciliation. */
export const JAVASCRIPT_RUNTIME_RECONCILIATION_PROVIDER = {
  id: "hurea-javascript-runtime-reconciliation",
  name: "HUREA JavaScript runtime reconciliation",
  version: "1",
} as const;

/** Provider identity for graph-native feature tracing and version comparison. */
export const JAVASCRIPT_APPLICATION_WORKFLOW_PROVIDER = {
  id: "hurea-javascript-application-workflows",
  name: "HUREA JavaScript application workflows",
  version: "1",
} as const;

/** Provider identity for deterministic cross-artifact comparisons. */
export const ARTIFACT_COMPARISON_PROVIDER = {
  id: "hurea-artifact-comparison",
  name: "HUREA artifact comparison",
  version: "1",
} as const;

/** Provider identity for deterministic cross-function comparisons. */
export const FUNCTION_COMPARISON_PROVIDER = {
  id: "hurea-function-comparison",
  name: "HUREA function comparison",
  version: "1",
} as const;

/** Provider identity for deterministic Evidence bundle comparisons. */
export const BUNDLE_COMPARISON_PROVIDER = {
  id: "hurea-bundle-comparison",
  name: "HUREA Evidence bundle comparison",
  version: "1",
} as const;

/** Provider identity for comparison-Evidence behavior aggregation. */
export const CHANGED_BEHAVIOR_PROVIDER = {
  id: "hurea-changed-behavior",
  name: "HUREA changed behavior investigation",
  version: "1",
} as const;

/** Provider identity for Evidence-backed call-path reconstruction. */
export const CALL_PATH_PROVIDER = {
  id: "hurea-call-path",
  name: "HUREA call path reconstruction",
  version: "1",
} as const;

/** Provider identity for explicit static/runtime hypothesis correlation. */
export const STATIC_RUNTIME_PROVIDER = {
  id: "hurea-static-runtime-correlation",
  name: "HUREA static/runtime correlation",
  version: "1",
} as const;

/** Provider identity for finite reconstruction specification verification. */
export const RECONSTRUCTION_PROVIDER = {
  id: "hurea-reconstruction-verifier",
  name: "HUREA reconstruction verifier",
  version: "1",
} as const;
