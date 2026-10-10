export const LARGE_FIXTURE_COUNT: number;
export const HOPPER_C_ORACLE: Readonly<{
  mainProcedure: "main";
  entryProcedure: "hurea_entry";
  branchProcedure: "hurea_branch";
  leafProcedure: "hurea_leaf";
  entryString: "HUREA_C_ENTRY";
  leafString: "HUREA_C_LEAF";
  globalName: "hurea_c_global";
}>;
export function sha256(value: string | Uint8Array): string;
export function generateLargeFixture(): string;
export function sourceDigest(
  sources: readonly { readonly path: string; readonly content: string }[],
): string;
