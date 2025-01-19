/** @type {FromMarkdownExtension[]} */
export const mdxFromMarkdown: FromMarkdownExtension[]
/** @type {ToMarkdownExtension} */
export const mdxToMarkdown: ToMarkdownExtension
export type FromMarkdownExtension = import('mdast-util-from-markdown').Extension
export type ToMarkdownExtension = import('mdast-util-to-markdown').Options
export type MDXFlowExpression =
  import('mdast-util-mdx-expression').MDXFlowExpression
export type MDXTextExpression =
  import('mdast-util-mdx-expression').MDXTextExpression
export type MDXJsxAttributeValueExpression =
  import('mdast-util-mdx-jsx').MDXJsxAttributeValueExpression
export type MDXJsxAttribute = import('mdast-util-mdx-jsx').MDXJsxAttribute
export type MDXJsxExpressionAttribute =
  import('mdast-util-mdx-jsx').MDXJsxExpressionAttribute
export type MDXJsxFlowElement = import('mdast-util-mdx-jsx').MDXJsxFlowElement
export type MDXJsxTextElement = import('mdast-util-mdx-jsx').MDXJsxTextElement
export type MDXJSEsm = import('mdast-util-mdxjs-esm').MDXJSEsm
