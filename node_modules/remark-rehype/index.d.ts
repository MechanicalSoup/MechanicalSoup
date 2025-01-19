export default remarkRehype
export type Node = import('unist').Node
export type HastRoot = import('hast').Root
export type MdastRoot = import('mdast').Root
export type Options = import('mdast-util-to-hast').Options
export type Processor = import('unified').Processor<any, any, any, any>
export type DoNotTouchAsThisImportIncludesRawInTree =
  typeof import('mdast-util-to-hast')
/**
 * Plugin to bridge or mutate to rehype.
 *
 * If a destination is given, runs the destination with the new hast tree
 * (bridge-mode).
 * Without destination, returns the hast tree: further plugins run on that tree
 * (mutate-mode).
 *
 * @param destination
 *   Optional unified processor.
 * @param options
 *   Options passed to `mdast-util-to-hast`.
 */
declare const remarkRehype: import('unified').Plugin<
  [Processor, Options?] | [Options] | [],
  MdastRoot
>
