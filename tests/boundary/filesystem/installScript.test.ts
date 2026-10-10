import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { describe, expect, it } from "vitest";

const run = promisify(execFile);

describe("HUREA local installer", () => {
  it("prints a local plan without installing dependencies or fetching a release", async () => {
    const result = await run("bash", ["install.sh", "--dry-run"], {
      env: { PATH: "/usr/bin:/bin" },
    });
    expect(result.stdout).toContain("HUREA local install plan");
    expect(result.stdout).toContain("Source:");
    expect(result.stdout).toContain("link hurea");
    expect(result.stderr).toBe("");
  });

  it("allows disabling interactive setup in a dry run", async () => {
    await expect(
      run("bash", ["install.sh", "--no-setup", "--dry-run"]),
    ).resolves.toMatchObject({ stderr: "" });
  });

  it("rejects obsolete remote-release options before any installation", async () => {
    await expect(
      run("bash", ["install.sh", "--version", "0.3.0"]),
    ).rejects.toMatchObject({ code: 1, stderr: "Unknown option: --version\n" });
  });
});
