/**
 * @typedef {import('unist').Node} Node
 * @typedef {import('hast').Root} HastRoot
 * @typedef {import('mdast').Root} MdastRoot
 * @typedef {import('mdast-util-to-hast').Options} Options
 * @typedef {import('unified').Processor<any, any, any, any>} Processor
 *
 * @typedef {import('mdast-util-to-hast')} DoNotTouchAsThisImportIncludesRawInTree
 */

import {toHast} from 'mdast-util-to-hast'

// Note: the `<MdastRoot, HastRoot>` overload doesn’t seem to work :'(

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
const remarkRehype =
  /** @type {(import('unified').Plugin<[Processor, Options?]|[Options]|[], MdastRoot>)} */
  (
    function (destination, options) {
      return destination && 'run' in destination
        ? bridge(destination, options)
        : mutate(destination)
    }
  )

export default remarkRehype

/**
 * Bridge-mode.
 * Runs the destination with the new hast tree.
 *
 * @type {import('unified').Plugin<[Processor, Options?], MdastRoot>}
 */
function bridge(destination, options) {
  return (node, file, next) => {
    destination.run(toHast(node, options), file, (error) => {
      next(error)
    })
  }
}

/**
 * Mutate-mode.
 * Further transformers run on the nlcst tree.
 *
 * @type {import('unified').Plugin<[Options?]|void[], MdastRoot, HastRoot>}
 */
function mutate(options) {
  // @ts-expect-error: assume a corresponding node is returned for `toHast`.
  return (node) => toHast(node, options)
}
