'use strict'

/**
 * Webpack loader
 *
 * @remarks
 * To do: once webpack supports ESM loaders, remove this wrapper.
 *
 * @param {string} code
 */
module.exports = function (code) {
  const callback = this.async()
  // Note that `import()` caches, so this should be fast enough.
  import('./lib/integration/webpack.js').then((module) =>
    module.loader.call(this, code, callback)
  )
}
