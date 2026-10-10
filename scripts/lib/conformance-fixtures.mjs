import { createHash } from "node:crypto";

export const LARGE_FIXTURE_COUNT = 1_205;

export const HOPPER_C_ORACLE = Object.freeze({
  mainProcedure: "main",
  entryProcedure: "hurea_entry",
  branchProcedure: "hurea_branch",
  leafProcedure: "hurea_leaf",
  entryString: "HUREA_C_ENTRY",
  leafString: "HUREA_C_LEAF",
  globalName: "hurea_c_global",
});

export const sha256 = (value) =>
  createHash("sha256").update(value).digest("hex");

export const generateLargeFixture = () => {
  const declarations = Array.from(
    { length: LARGE_FIXTURE_COUNT },
    (_, index) =>
      `__attribute__((noinline, used)) int hurea_inventory_${String(index).padStart(4, "0")}(void) { puts("HUREA_INVENTORY_${String(index).padStart(4, "0")}"); return ${index}; }`,
  );
  return [
    "#include <stdio.h>",
    ...declarations,
    "int main(void) { return hurea_inventory_0000(); }",
    "",
  ].join("\n");
};

export const sourceDigest = (sources) => {
  const canonical = [...sources]
    .sort(({ path: left }, { path: right }) => left.localeCompare(right))
    .map(({ path, content }) => `${path}\0${sha256(content)}\n`)
    .join("");
  return sha256(canonical);
};
