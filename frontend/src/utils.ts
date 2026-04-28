import DOMPurify from "dompurify";
import katex from "katex";
import { marked } from "marked";

function renderKatex(markdown: string): string {
  const placeholders: string[] = [];

  const storeFormula = (formula: string, displayMode: boolean): string => {
    const rendered = katex.renderToString(formula.trim(), {
      displayMode,
      throwOnError: false,
      strict: "ignore",
    });
    const token = `KATEX_PLACEHOLDER_${placeholders.length}`;
    placeholders.push(rendered);
    return token;
  };

  const withBlocks = markdown.replace(/\$\$([\s\S]+?)\$\$/g, (_, formula: string) =>
    `\n\n${storeFormula(formula, true)}\n\n`,
  );

  const withInline = withBlocks.replace(/(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)/g, (_, formula: string) =>
    storeFormula(formula, false),
  );

  return placeholders.reduce(
    (result, html, index) => result.split(`KATEX_PLACEHOLDER_${index}`).join(html),
    withInline,
  );
}

export function formatTimestamp(timestamp: number): string {
  return new Date(timestamp * 1000).toLocaleString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function renderMarkdown(markdown: string): string {
  const markdownWithKatex = renderKatex(markdown);
  const rawHtml = marked.parse(markdownWithKatex, {
    breaks: true,
    gfm: true,
  }) as string;
  return DOMPurify.sanitize(rawHtml);
}
