import { describe, expect, it } from "vitest";

import { parseConfig } from "./config.js";

describe("capability flags", () => {
  it("rejects values outside the exact true/false boundary", () => {
    for (const key of [
      "HUREA_PROCESS_CAPTURE_ENABLED",
      "HUREA_BROWSER_OBSERVE_ENABLED",
      "HUREA_BROWSER_SCENARIO_ENABLED",
      "HUREA_ELECTRON_OBSERVE_ENABLED",
      "HUREA_ELECTRON_AUTOMATE_ENABLED",
      "HUREA_V8_INSPECTOR_OBSERVE_ENABLED",
      "HUREA_JAVASCRIPT_REPLAY_ENABLED",
      "HUREA_MANAGED_RUNTIME_ENABLED",
    ]) {
      const result = parseConfig({ [key]: "typo" });
      expect(result.ok, key).toBe(false);
    }
  });
});
