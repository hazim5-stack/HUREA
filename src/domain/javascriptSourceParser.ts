import { parse } from "@babel/parser";

/** Babel AST produced by HUREA's inert JavaScript parser boundary. */
export type ParsedJavaScriptSource = ReturnType<typeof parse>;

/** Parse JavaScript or TypeScript once without retaining unused comment nodes. */
export const parseJavaScriptSource = (
  source: string,
): ParsedJavaScriptSource | null => {
  try {
    return parse(source, {
      sourceType: "unambiguous",
      errorRecovery: true,
      attachComment: false,
      plugins: ["jsx", "typescript"],
    });
  } catch {
    return null;
  }
};
