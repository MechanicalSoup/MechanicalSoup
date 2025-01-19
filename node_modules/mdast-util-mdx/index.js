/**
 * @typedef {import('mdast-util-from-markdown').Extension} FromMarkdownExtension
 * @typedef {import('mdast-util-to-markdown').Options} ToMarkdownExtension
 * @typedef {import('mdast-util-mdx-expression').MDXFlowExpression} MDXFlowExpression
 * @typedef {import('mdast-util-mdx-expression').MDXTextExpression} MDXTextExpression
 * @typedef {import('mdast-util-mdx-jsx').MDXJsxAttributeValueExpression} MDXJsxAttributeValueExpression
 * @typedef {import('mdast-util-mdx-jsx').MDXJsxAttribute} MDXJsxAttribute
 * @typedef {import('mdast-util-mdx-jsx').MDXJsxExpressionAttribute} MDXJsxExpressionAttribute
 * @typedef {import('mdast-util-mdx-jsx').MDXJsxFlowElement} MDXJsxFlowElement
 * @typedef {import('mdast-util-mdx-jsx').MDXJsxTextElement} MDXJsxTextElement
 * @typedef {import('mdast-util-mdxjs-esm').MDXJSEsm} MDXJSEsm
 */

import {
  mdxExpressionFromMarkdown,
  mdxExpressionToMarkdown
} from 'mdast-util-mdx-expression'
import {mdxJsxFromMarkdown, mdxJsxToMarkdown} from 'mdast-util-mdx-jsx'
import {mdxjsEsmFromMarkdown, mdxjsEsmToMarkdown} from 'mdast-util-mdxjs-esm'

/** @type {FromMarkdownExtension[]} */
export const mdxFromMarkdown = [
  mdxExpressionFromMarkdown,
  mdxJsxFromMarkdown,
  mdxjsEsmFromMarkdown
]

/** @type {ToMarkdownExtension} */
export const mdxToMarkdown = {
  extensions: [mdxExpressionToMarkdown, mdxJsxToMarkdown, mdxjsEsmToMarkdown]
}
