/** @type {FromMarkdownExtension} */
export const mdxJsxFromMarkdown: FromMarkdownExtension
/** @type {ToMarkdownExtension} */
export const mdxJsxToMarkdown: ToMarkdownExtension
export type Literal = import('mdast').Literal
export type Parent = import('mdast').Parent
export type FromMarkdownExtension = import('mdast-util-from-markdown').Extension
export type FromMarkdownHandle = import('mdast-util-from-markdown').Handle
export type Token = import('mdast-util-from-markdown').Token
export type ToMarkdownExtension = import('mdast-util-to-markdown').Options
export type ToMarkdownHandle = import('mdast-util-to-markdown').Handle
export type ToMarkdownMap = import('mdast-util-to-markdown').Map
export type OnEnterError = import('mdast-util-from-markdown').OnEnterError
export type OnExitError = import('mdast-util-from-markdown').OnExitError
export type Program = import('estree-jsx').Program
export type MdxJsxAttributeValueExpression =
  import('./complex-types').MdxJsxAttributeValueExpression
export type MdxJsxAttribute = import('./complex-types').MdxJsxAttribute
export type MdxJsxExpressionAttribute =
  import('./complex-types').MdxJsxExpressionAttribute
export type MdxJsxFlowElement = import('./complex-types').MdxJsxFlowElement
export type MdxJsxTextElement = import('./complex-types').MdxJsxTextElement
export type Tag = {
  name: string | null
  attributes: (MdxJsxAttribute | MdxJsxExpressionAttribute)[]
  close?: boolean
  selfClosing?: boolean
  start: Token['start']
  end: Token['start']
}
/**
 * Legacy names:
 */
export type MDXJsxAttributeValueExpression = MdxJsxAttributeValueExpression
/**
 * Legacy names:
 */
export type MDXJsxAttribute = MdxJsxAttribute
/**
 * Legacy names:
 */
export type MDXJsxExpressionAttribute = MdxJsxExpressionAttribute
/**
 * Legacy names:
 */
export type MDXJsxFlowElement = MdxJsxFlowElement
/**
 * Legacy names:
 */
export type MDXJsxTextElement = MdxJsxTextElement
