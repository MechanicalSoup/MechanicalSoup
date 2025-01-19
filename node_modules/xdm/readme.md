# xdm

[![Build][build-badge]][build]
[![Coverage][coverage-badge]][coverage]
[![Downloads][downloads-badge]][downloads]
[![Size][size-badge]][size]

**xdm** is an MDX compiler that focusses on two things:

1.  Compiling the MDX syntax (markdown + JSX) to JavaScript
2.  Making it easier to use the MDX syntax in different places

This is mostly things I wrote for `@mdx-js/mdx` which are not slated to be
released (soon?) plus some further changes that I think are good ideas (source
maps, ESM only, defaulting to an automatic JSX runtime, no Babel, smallish
browser size, more docs, import/exports in evaluate, esbuild and Rollup
plugins).

There are also some cool experimental features in [👩‍🔬 Lab][lab]!

## Install

Use Node 12 or later.
Then install `xdm` with either npm or yarn.

[npm][]:

```sh
npm install xdm
```

[yarn][]:

```sh
yarn add xdm
```

This package is [ESM only](https://gist.github.com/sindresorhus/a39789f98801d908bbc7ff3ecc99d99c):
Node 12+ is needed to use it and it must be `import`ed instead of `require`d.

## Contents

*   [What is MDX?](#what-is-mdx)
*   [Use](#use)
*   [API](#api)
    *   [`compile(file, options?)`](#compilefile-options)
    *   [`compileSync(file, options?)`](#compilesyncfile-options)
    *   [`evaluate(file, options)`](#evaluatefile-options)
    *   [`evaluateSync(file, options)`](#evaluatesyncfile-options)
    *   [`createProcessor(options)`](#createprocessoroptions)
*   [👩‍🔬 Lab](#-lab)
    *   [Importing `.mdx` files directly](#importing-mdx-files-directly)
    *   [Requiring `.mdx` files directly](#requiring-mdx-files-directly)
    *   [Importing `.md` and `.mdx` files from the web in esbuild](#importing-md-and-mdx-files-from-the-web-in-esbuild)
*   [MDX syntax](#mdx-syntax)
    *   [Markdown](#markdown)
    *   [JSX](#jsx)
    *   [ESM](#esm)
    *   [Expressions](#expressions)
*   [MDX content](#mdx-content)
    *   [Components](#components)
    *   [Layout](#layout)
*   [Integrations](#integrations)
    *   [Bundlers](#bundlers)
    *   [Build systems](#build-systems)
    *   [Compilers](#compilers)
    *   [Site generators](#site-generators)
    *   [Hyperscript implementations (frameworks)](#hyperscript-implementations-frameworks)
    *   [Runtime libraries](#runtime-libraries)
*   [Guides](#guides)
    *   [GitHub flavored markdown (GFM)](#github-flavored-markdown-gfm)
    *   [Syntax highlighting](#syntax-highlighting)
    *   [Math](#math)
    *   [Footnotes](#footnotes)
    *   [Frontmatter](#frontmatter)
*   [Plugins](#plugins)
*   [Types](#types)
*   [Differences from `@mdx-js/mdx`](#differences-from-mdx-jsmdx)
*   [Architecture](#architecture)
*   [Security](#security)
*   [Related](#related)
*   [License](#license)

## What is MDX?

MDX is different things.
The term is sometimes used for a compiler, typically implying `@mdx-js/mdx`, but
there are more.
First there was [`mdxc`][mdxc].
Then came [`@mdx-js/mdx`][mdxjs].
There’s also [`mdsvex`][mdsvex].
And now there’s **xdm** too.

Sometimes the term is used for a runtime/helper library.
**xdm** has **no runtime**: it’s not needed!

Most often the term is used for the format: markdown + JS(X) (there are some
[caveats][]):

```mdx
## Hello, world!

<div className="note">
  > Some notable things in a block quote!
</div>
```

See?
Most of markdown works!
Those XML-like things are not HTML though: they’re JSX.
Note that there are some differences in how JSX should be authored: for example,
React expects `className`, whereas Vue expects `class`.
See [§ MDX syntax][mdx-syntax] below for more on how the format works.

## Use

This section describes how to use the API.
See [§ MDX syntax][mdx-syntax] on how the format works.
See [§ Integrations][integrations] on how to use **xdm** with Babel, esbuild,
Rollup, webpack, etc.

Say we have an MDX document, `example.mdx`:

```mdx
export const Thing = () => <>World!</>

# Hello, <Thing />
```

First, a rough idea of what the result will be.
The below is not the actual output, but it might help to form a mental model:

```js
/* @jsxRuntime automatic @jsxImportSource react */

export const Thing = () => <>World!</>

export default function MDXContent() {
  return <h1>Hello, <Thing /></h1>
}
```

Some observations:

*   The output is serialized JavaScript that still needs to be evaluated
*   A comment is injected to configure how JSX is handled
*   It’s a complete file with import/exports
*   A component (`MDXContent`) is exported

Now for how to get the actual output.
Add some code in `example.js` to compile `example.mdx` to JavaScript:

```js
import {promises as fs} from 'node:fs'
import {compile} from 'xdm'

main()

async function main() {
  const compiled = await compile(await fs.readFile('example.mdx'))
  console.log(String(compiled))
}
```

The *actual* output of running `node example.js` is:

```js
/* @jsxRuntime automatic @jsxImportSource react */
import {Fragment as _Fragment, jsx as _jsx, jsxs as _jsxs} from 'react/jsx-runtime'

export const Thing = () => _jsx(_Fragment, {children: 'World!'})

function MDXContent(props = {}) {
  const _components = Object.assign({h1: 'h1'}, props.components)
  const {wrapper: MDXLayout} = _components
  const _content = _jsx(_Fragment, {
    children: _jsxs(_components.h1, {
      children: ['Hello, ', _jsx(Thing, {})]
    })
  })
  return MDXLayout
    ? _jsx(MDXLayout, Object.assign({}, props, {children: _content}))
    : _content
}

export default MDXContent
```

Some more observations:

*   JSX is compiled away to function calls and an import of React†
*   The content component can be given `{components: {h1: MyComponent}}` to use
    something else for the heading
*   The content component can be given `{components: {wrapper: MyLayout}}` to
    wrap the whole content

† **xdm** is not coupled to React.
You can also use it with [Preact](#preact), [Vue](#vue), [Emotion](#emotion),
[Theme UI](#theme-ui), etc.

See [§ MDX content][mdx-content] below on how to use the result.

## API

`xdm` exports the following identifiers:
[`compile`][compile],
[`compileSync`](#compilesyncfile-options),
[`evaluate`][eval],
[`evaluateSync`](#evaluatesyncfile-options), and
[`createProcessor`](#createprocessoroptions).
There is no default export.

`xdm/esbuild.js` exports a function as the default export that returns an
[esbuild][] plugin.

`xdm/rollup.js` exports a function as the default export that returns a
[Rollup][] plugin.

`xdm/webpack.cjs` exports a [webpack][] loader as the default export.

There is also `xdm/esm-loader.js` and `xdm/register.cjs`, see [👩‍🔬 Lab][lab]
for more info.

### `compile(file, options?)`

Compile MDX to JS.

###### `file`

MDX document to parse (`string`, [`Buffer`][buffer] in UTF-8, [`vfile`][vfile],
or anything that can be given to `vfile`).

<details>
<summary>Example</summary>

```js
import {VFile} from 'vfile'
import {compile} from 'xdm'

await compile(':)')
await compile(Buffer.from(':-)'))
await compile({path: 'path/to/file.mdx', value: '🥳'})
await compile(new VFile({path: 'path/to/file.mdx', value: '🤭'}))
```

</details>

###### `options.remarkPlugins`

List of [remark plugins][remark-plugins], presets, and pairs.

<details>
<summary>Example</summary>

```js
import remarkFrontmatter from 'remark-frontmatter' // YAML and such.
import remarkGfm from 'remark-gfm' // Tables, strikethrough, tasklists, literal URLs.

await compile(file, {remarkPlugins: [remarkGfm]}) // One plugin.
await compile(file, {remarkPlugins: [[remarkFrontmatter, 'toml']]}) // A plugin with options.
await compile(file, {remarkPlugins: [remarkGfm, remarkFrontmatter]}) // Two plugins.
await compile(file, {remarkPlugins: [[remarkGfm, {singleTilde: false}], remarkFrontmatter]}) // Two plugins, first w/ options.
```

</details>

###### `options.rehypePlugins`

List of [rehype plugins][rehype-plugins], presets, and pairs.

<details>
<summary>Example</summary>

```js
import rehypeKatex from 'rehype-katex' // Render math with KaTeX.
import remarkMath from 'remark-math' // Support math like `$so$`.

await compile(file, {remarkPlugins: [remarkMath], rehypePlugins: [rehypeKatex]})

await compile(file, {
  remarkPlugins: [remarkMath],
  // A plugin with options:
  rehypePlugins: [[rehypeKatex, {throwOnError: true, strict: true}]]
})
```

</details>

###### `options.recmaPlugins`

List of recma plugins.
This is a new ecosystem, currently in beta, to transform
[esast](https://github.com/syntax-tree/esast) trees (JavaScript).

###### `options.mdExtensions`

List of markdown extensions, with dot (`string[]`, default: `['.md',
'.markdown', '.mdown', '.mkdn', '.mkd', '.mdwn', '.mkdown', '.ron']`).

###### `options.mdxExtensions`

List of MDX extensions, with dot (`string[]`, default: `['.mdx']`).
Has no effect in `compile` or `evaluate`, but does affect [esbuild][],
[Rollup][], and the experimental ESM loader + register hook (see [👩‍🔬
Lab][lab]).

###### `options.format`

Format the file is in (`'detect' | 'mdx' | 'md'`, default: `'detect'`).

*   `'detect'` — use `'markdown'` for files with an extension in `mdExtensions`
    and `'mdx'` otherwise
*   `'mdx'` — treat file as [MDX][mdx-syntax]
*   `'md'` — treat file as plain vanilla markdown

The format cannot be detected if a file is passed without a path or extension:
`mdx` will be assumed.
So pass a full vfile (with `path`) or an object with a path.

<details>
<summary>Example</summary>

```js
compile({value: '…'}) // Seen as MDX
compile({value: '…'}, {format: 'md'}) // Seen as markdown
compile({value: '…', path: 'readme.md'}) // Seen as markdown

// Please do not use `.md` for MDX as other tools won’t know how to handle it.
compile({value: '…', path: 'readme.md'}, {format: 'mdx'}) // Seen as MDX
compile({value: '…', path: 'readme.md'}, {mdExtensions: []}) // Seen as MDX
```

</details>

This option mostly affects [esbuild][] and [Rollup][] plugins, and the
experimental ESM loader + register hook (see [👩‍🔬 Lab][lab]), because in those
it affects *which* files are “registered”:

*   `format: 'mdx'` registers the extensions in `options.mdxExtensions`
*   `format: 'md'` registers the extensions in `options.mdExtensions`
*   `format: 'detect'` registers both lists of extensions

###### `options.outputFormat`

Output format to generate (`'program' | 'function-body'`, default: `'program'`).
In most cases `'program'` should be used, as it results in a whole program.
Internally, [`evaluate`][eval] uses `outputFormat: 'function-body'` to compile
to code that can be `eval`ed.
In some cases, you might want to do what `evaluate` does in separate steps
yourself, such as when compiling on the server and running on the client.

The `'program'` format will use import statements to import the runtime (and
optionally provider) and use an export statement to yield the `MDXContent`
component.

The `'function-body'` format will get the runtime (and optionally provider) from
`arguments[0]`, rewrite export statements, and use a return statement to yield
what was exported.
Normally, this output format will throw on `import` (and `export … from`)
statements, but you can support them by setting
[`options.useDynamicImport`][usedynamicimport].

<details>
<summary>Example</summary>

A module `example.js`:

```js
import {compile} from 'xdm'

main('export const no = 3.14\n\n# hi {no}')

async function main(code) {
  console.log(String(await compile(code, {outputFormat: 'program'}))) // Default
  console.log(String(await compile(code, {outputFormat: 'function-body'})))
}
```

…yields:

```js
import {Fragment as _Fragment, jsx as _jsx} from 'react/jsx-runtime'
export const no = 3.14
function MDXContent(props = {}) { /* … */ }
export default MDXContent
```

```js
const {Fragment: _Fragment, jsx: _jsx} = arguments[0]
const no = 3.14
function MDXContent(props = {}) { /* … */ }
return {no, default: MDXContent}
```

</details>

###### `options.useDynamicImport`

Whether to compile to dynamic import expressions (`boolean`, default: `false`).
This option applies when [`options.outputFormat`][outputformat] is
`'function-body'`.

**xdm** can turn import statements (`import x from 'y'`) into dynamic imports
(`const {x} = await import('y')`).
This is useful because import statements only work at the top level of
JavaScript modules, whereas `import()` is available inside function bodies.

When you turn `useDynamicImport` on, you should probably set [`options.baseUrl`][baseurl] too.

<details>
<summary>Example</summary>

Say we have a couple modules:

```js
// meta.js:
export const title = 'World'

// numbers.js:
export const no = 3.14

// example.js:
import {compileSync} from 'xdm'

const code = `import {name} from './meta.js'
export {no} from './numbers.js'

# hi {name}!`

console.log(String(compileSync(code, {outputFormat: 'function-body', useDynamicImport: true})))
```

…now running `node example.js` yields:

```js
const {Fragment: _Fragment, jsx: _jsx, jsxs: _jsxs} = arguments[0]
const {name} = await import('./meta.js')
const {no} = await import('./numbers.js')
function MDXContent(props = {}) { /* … */ }
return {no, default: MDXContent}
```

</details>

###### `options.baseUrl`

Resolve relative `import` (and `export … from`) from this URL (`string?`,
example: `import.meta.url`).

Relative specifiers are non-absolute URLs that start with `/`, `./`, or `../`.
For example: `/index.js`, `./folder/file.js`, or `../main.js`.

This option is useful when code will run in a different place.
One example is when `.mdx` files are in path *a* but compiled to path *b* and
imports should run relative the path *b*.
Another example is when evaluating code, whether in Node or a browser.

<details>
<summary>Example</summary>

Say we have a module `example.js`:

```js
import {compile} from 'xdm'

main()

async function main() {
  const code = 'export {number} from "./data.js"\n\n# hi'
  const baseUrl = 'https://a.full/url' // Typically `import.meta.url`
  console.log(String(await compile(code, {baseUrl})))
}
```

…now running `node example.js` yields:

```js
import {Fragment as _Fragment, jsx as _jsx} from 'react/jsx-runtime'
export {number} from 'https://a.full/data.js'
function MDXContent(props = {}) { /* … */ }
export default MDXContent
```

</details>

###### `options.SourceMapGenerator`

The `SourceMapGenerator` class from [`source-map`][source-map] (optional).
When given, the resulting file will have a `map` field set to a source map (in
object form).

<details>
<summary>Example</summary>

Assuming `example.mdx` from [§ Use][use] exists, then:

```js
import {promises as fs} from 'node:fs'
import {SourceMapGenerator} from 'source-map'
import {compile} from 'xdm'

main()

async function main() {
  const file = await compile(
    {path: 'example.mdx', value: await fs.readFile('example.mdx')},
    {SourceMapGenerator}
  )

  console.log(file.map)
}
```

…yields:

```js
{
  version: 3,
  sources: ['example.mdx'],
  names: ['Thing'],
  mappings: ';;aAAaA,QAAQ;YAAQ;;;;;;;;iBAE3B',
  file: 'example.mdx'
}
```

</details>

###### `options.providerImportSource`

Place to import a provider from (`string?`, example: `'@mdx-js/react'`).
Useful for runtimes that support context (React, Preact).
The provider must export a `useMDXComponents`, which is called to access an
object of components.

<details>
<summary>Example</summary>

If `file` is the contents of `example.mdx` from [§ Use][use], then:

```js
compile(file, {providerImportSource: '@mdx-js/react'})
```

…yields this difference:

```diff
 /* @jsxRuntime classic @jsx React.createElement @jsxFrag React.Fragment */
 import React from 'react'
+import {useMDXComponents as _provideComponents} from '@mdx-js/react'

 export const Thing = () => React.createElement(React.Fragment, null, 'World!')

 function MDXContent(props = {}) {
-  const _components = Object.assign({h1: 'h1'}, props.components)
+  const _components = Object.assign({h1: 'h1'}, _provideComponents(), props.components)
   const {wrapper: MDXLayout} = _components
   const _content = React.createElement(
     React.Fragment,
```

</details>

###### `options.jsx`

Whether to keep JSX (`boolean?`, default: `false`).
The default is to compile JSX away so that the resulting file is immediately
runnable.

<details>
<summary>Example</summary>

If `file` is the contents of `example.mdx` from [§ Use][use], then:

```js
compile(file, {jsx: true})
```

…yields this difference:

```diff
 /* @jsxRuntime classic @jsx React.createElement @jsxFrag React.Fragment */
-import {Fragment as _Fragment, jsx as _jsx, jsxs as _jsxs} from 'react/jsx-runtime'
-
-export const Thing = () => React.createElement(React.Fragment, null, 'World!')
+export const Thing = () => <>World!</>

 function MDXContent(props = {}) {
   const _components = Object.assign({h1: 'h1'}, props.components)
   const {wrapper: MDXLayout} = _components
-  const _content = _jsx(_Fragment, {
-    children: _jsxs(_components.h1, {
-      children: ['Hello, ', _jsx(Thing, {})]
-    })
-  })
+  const _content = (
+    <>
+      <_components.h1>{'Hello, '}<Thing /></_components.h1>
+    </>
+  )
…
```

</details>

###### `options.jsxRuntime`

JSX runtime to use (`'automatic' | 'classic'`, default: `'automatic'`).
The classic runtime compiles to calls such as `h('p')`, the automatic runtime
compiles to `import _jsx from '$importSource/jsx-runtime'\n_jsx('p')`.

<details>
<summary>Example</summary>

If `file` is the contents of `example.mdx` from [§ Use][use], then:

```js
compile(file, {jsxRuntime: 'classic'})
```

…yields this difference:

```diff
-/* @jsxRuntime automatic @jsxImportSource react */
-import {Fragment as _Fragment, jsx as _jsx, jsxs as _jsxs} from 'react/jsx-runtime'
+/* @jsxRuntime classic @jsx React.createElement @jsxFrag React.Fragment */
+import React from 'react'

-export const Thing = () => _jsx(_Fragment, {children: 'World!'})
+export const Thing = () => React.createElement(React.Fragment, null, 'World!')
…
```

</details>

###### `options.jsxImportSource`

Place to import automatic JSX runtimes from (`string?`, default: `'react'`).
When in the `automatic` runtime, this is used to define an import for
`_Fragment`, `_jsx`, and `_jsxs`.

<details>
<summary>Example</summary>

If `file` is the contents of `example.mdx` from [§ Use][use], then:

```js
compile(file, {jsxImportSource: 'preact'})
```

…yields this difference:

```diff
-/* @jsxRuntime automatic @jsxImportSource react */
-import {Fragment as _Fragment, jsx as _jsx, jsxs as _jsxs} from 'react/jsx-runtime'
+/* @jsxRuntime automatic @jsxImportSource preact */
+import {Fragment as _Fragment, jsx as _jsx, jsxs as _jsxs } from 'preact/jsx-runtime'
```

</details>

###### `options.pragma`

Pragma for JSX (`string?`, default: `'React.createElement'`).
When in the `classic` runtime, this is used as an identifier for function calls:
`<x />` to `React.createElement('x')`.

You should most probably define `pragmaFrag` and `pragmaImportSource` too when
changing this.

<details>
<summary>Example</summary>

If `file` is the contents of `example.mdx` from [§ Use][use], then:

```js
compile(file, {
  jsxRuntime: 'classic',
  pragma: 'preact.createElement',
  pragmaFrag: 'preact.Fragment',
  pragmaImportSource: 'preact/compat'
})
```

…yields this difference:

```diff
-/* @jsxRuntime classic @jsx React.createElement @jsxFrag React.Fragment */
-import React from 'react'
+/* @jsxRuntime classic @jsx preact.createElement @jsxFrag preact.Fragment */
+import preact from 'preact/compat'

-export const Thing = () => React.createElement(React.Fragment, null, 'World!')
+export const Thing = () => preact.createElement(preact.Fragment, null, 'World!')
…
```

</details>

###### `options.pragmaFrag`

Pragma for JSX fragments (`string?`, default: `'React.Fragment'`).
When in the `classic` runtime, this is used as an identifier for fragments: `<>`
to `React.createElement(React.Fragment)`.

See `options.pragma` for an example.

###### `options.pragmaImportSource`

Where to import the identifier of `pragma` from (`string?`, default: `'react'`).
When in the `classic` runtime, this is used to import the `pragma` function.
To illustrate with an example: when `pragma` is `'a.b'` and `pragmaImportSource`
is `'c'` this following will be generated: `import a from 'c'`.

See `options.pragma` for an example.

###### Returns

`Promise.<VFile>` — Promise that resolves to the compiled JS as a [vfile][].

<details>
<summary>Example</summary>

```js
import remarkPresetLintConsistent from 'remark-preset-lint-consistent' // Lint rules to check for consistent markdown.
import {reporter} from 'vfile-reporter'
import {compile} from 'xdm'

main()

async function main() {
  const file = await compile('*like this* or _like this_?', {remarkPlugins: [remarkPresetLintConsistent]})
  console.error(reporter(file))
}
```

Yields:

```txt
  1:16-1:27  warning  Emphasis should use `*` as a marker  emphasis-marker  remark-lint

⚠ 1 warning
```

</details>

### `compileSync(file, options?)`

Compile MDX to JS.
Synchronous version of `compile`.
When possible please use the async `compile`.

### `evaluate(file, options)`

Compile and run MDX.
☢️ It’s called **evaluate** because it `eval`s JavaScript.
When possible, please use `compile`, write to a file, and then run with Node or
bundle with [esbuild][]/[Rollup][]/[webpack][].
But if you trust your content, `evaluate` can work.

`evaluate` wraps code in an [`AsyncFunction`][async-function], `evaluateSync`
uses a normal [`Function`][function].
That means that `evaluate` also supports top-level await.

Typically, `import` (or `export … from`) do not work here.
They can be compiled to dynamic `import()` by passing
[`options.useDynamicImport`][usedynamicimport].

###### `file`

See [`compile`][compile].

###### `options`

Most options are the same as [`compile`][compile], with the following
exceptions:

*   `providerImportSource` is replaced by `useMDXComponents`
*   `jsx*` and `pragma*` options are replaced by `jsx`, `jsxs`, and `Fragment`
*   `outputFormat` is set to `function-body`

###### `options.jsx`

###### `options.jsxs`

###### `options.Fragment`

These three options are required.
They come from an automatic JSX runtime that you must import yourself.

<details>
<summary>Example</summary>

```js
import * as runtime from 'react/jsx-runtime.js'

const {default: Content} = await evaluate('# hi', {...runtime, ...otherOptions})
```

</details>

###### `options.useMDXComponents`

Needed if you want to support a provider.

<details>
<summary>Example</summary>

```js
import * as provider from '@mdx-js/react'
import * as runtime from 'react/jsx-runtime.js'

const {default: Content} = await evaluate('# hi', {...provider, ...runtime, ...otherOptions})
```

</details>

###### Returns

`Promise.<Object>` — Promise that resolves to something that looks a bit like a
module: an object with a `default` field set to the component and anything else
that was exported from the MDX file available too.

<details>
<summary>Example</summary>

Assuming the contents of `example.mdx` from [§ Use][use] was in `file`, then:

```js
import * as runtime from 'react/jsx-runtime.js'
import {evaluate} from 'xdm'

console.log(await evaluate(file, {...runtime}))
```

…yields:

```js
{Thing: [Function: Thing], default: [Function: MDXContent]}
```

</details>

### `evaluateSync(file, options)`

Compile and run MDX.
Synchronous version of [`evaluate`][eval].
When possible please use the async `evaluate`.

### `createProcessor(options)`

Create a unified processor to compile MDX to JS.
Has the same options as [`compile`][compile], but returns a configured
[`processor`](https://github.com/unifiedjs/unified#processor).

Note that `format: 'detect'` does not work here: only `'md'` or `'mdx'` are
allowed (and `'mdx'` is the default).

## 👩‍🔬 Lab

This section describes experimental features!
These do not adhere to semver and could break at any time!

### Importing `.mdx` files directly

[ESM loaders](https://nodejs.org/api/esm.html#esm\_loaders) are an experimental
feature in Node, slated to change.
Still, they let projects “hijack” imports, to do all sorts of fancy things!
**xdm** comes with experimental support for importing `.mdx` files with
on-the-fly compilation, using `xdm/esm-loader.js`:

Assuming `example.mdx` from [§ Use][use] exists, and our module `example.js`
looks as follows:

```js
import {renderToStaticMarkup} from 'react-dom/server.js'
import React from 'react'
import Content from './example.mdx'

console.log(renderToStaticMarkup(React.createElement(Content)))
```

Running that with:

```sh
node --experimental-loader=xdm/esm-loader.js example.js
```

…yields:

```html
<h1>Hello, World!</h1>
```

To pass options, you can make your own loader, such as this `my-loader.js`:

```js
import {createLoader} from 'xdm/esm-loader.js'

const {getFormat, transformSource} = createLoader(/* Options… */)

export {getFormat, transformSource}
```

Which can then be used with `node --experimental-loader=./my-loader.js`.

Node itself does not yet support multiple loaders, but it is possible to combine
multiple loaders with
[`@node-loader/core`](https://github.com/node-loader/node-loader-core).

### Requiring `.mdx` files directly

[`require.extensions`](https://nodejs.org/api/modules.html#modules\_require\_extensions)
is a deprecated feature in Node.
Still, it lets projects “hijack” `require` calls to do fancy things.
**xdm** comes with support for requiring `.mdx` files with on-the-fly
evaluation, using `xdm/register.cjs`:

Assuming `example.mdx` from [§ Use][use] exists, and our script `example.cjs`
looks as follows:

```js
const React = require('react')
const {renderToStaticMarkup} = require('react-dom/server.js')
const Content = require('./example.mdx')

console.log(renderToStaticMarkup(React.createElement(Content)))
```

Running that with:

```sh
node -r xdm/register.cjs example.cjs
```

…yields:

```html
<h1>Hello, World!</h1>
```

To pass options, you can make your own hook, such as this `my-hook.cjs`:

```js
'use strict'

const register = require('xdm/lib/integration/require.cjs')

register({/* Options… */})
```

Which can then be used with `node -r ./my-hook.cjs`.

The register hook uses [`evaluateSync`][eval].
That means `import` (and `export … from`) are not supported when requiring
`.mdx` files.

### Importing `.md` and `.mdx` files from the web in esbuild

> ⚠️ Note that this includes remote code in your bundle.
> Make sure you trust it!
> See [§ Security][security] for more info.

When passing `allowDangerousRemoteMdx` to the esbuild loader, MD(X) and JS files
can be imported from `http:` and `https:` urls.
Take this `index.mdx` file:

```jsx
import Readme from 'https://raw.githubusercontent.com/wooorm/xdm/main/readme.md'

Embed the xdm readme like so:

<Readme />
```

And a module `build.js`:

```js
import xdm from 'xdm/esbuild.js'
import esbuild from 'esbuild'

await esbuild.build({
  entryPoints: ['index.mdx'],
  outfile: 'output.js',
  format: 'esm',
  plugins: [xdm({allowDangerousRemoteMdx: true, /* Other options… */})]
})
```

Running that (`node build.js`) and evaluating `output.js` (depends on how you
evaluate React stuff) would give:

```jsx
<p>Embed the xdm readme like so:</p>
<h1>xdm</h1>
{/* … */}
<p><a href="https://github.com/wooorm/xdm/blob/main/license">MIT</a> © …</p>
```

## MDX syntax

> **Note**!
> You don’t have to use this syntax.
> Or use it always.
> With [`format`][format], you can opt-in gradually or not at all.

The MDX syntax is a mix between markdown and JSX.
Markdown often feels more natural to type than HTML (or JSX) for the common
things (like emphasis, headings).
JSX is an extension to JavaScript that *looks* like HTML but makes it convenient
to use components (reusable things).
See [this description](https://github.com/micromark/mdx-state-machine#71-syntax)
for a more formal description of the syntax.

This gives us something along the lines of [literate programming][lit].

MDX also gives us an odd mix of two languages: markdown is whitespace sensitive
and forgiving (what you type may not “work”, but it won’t crash) whereas
JavaScript is whitespace **insensitive** and **does** crash on typos.
Weirdly enough they combine pretty well!

It’s important to know markdown
([see this cheatsheet and tutorial](https://commonmark.org/help/) for help)
and have experience with JavaScript (specifically
[JSX](https://facebook.github.io/jsx/)) to write (and enjoy writing) MDX.

Some common gotchas with writing MDX are
[documented here](https://github.com/micromark/mdx-state-machine#74-common-mdx-gotchas).

### Markdown

Most of markdown ([CommonMark][]) works:

````mdx
# Heading (rank 1)
## Heading 2
### 3
#### 4
##### 5
###### 6

> Block quote

* Unordered
* List

1. Ordered
2. List

A paragraph, introducing a thematic break:

***

```js
some.code()
```

a [link](https://example.com), an ![image](./image.png), some *emphasis*,
something **strong**, and finally a little `code()`.
````

Some other features often used with markdown are:

*   **GFM** — autolink literals, strikethrough, tables, tasklists
    ([see guide below](#github-flavored-markdown-gfm))
*   **Frontmatter** — YAML
    ([see guide below](#frontmatter))
*   **Footnotes**
    ([see guide below](#footnotes))
*   **Math**
    ([see guide below](#math))
*   **Syntax highlighting**
    ([see guide below](#syntax-highlighting))

There are many more things possible by configuring
[remark plugins][remark-plugins] and [rehype plugins][rehype-plugins].

There are also a couple specific remark/rehype/recma plugins that work with
xdm: see [plugins][].

#### Caveats

Some markdown features don’t work in MDX:

```mdx
Indented code works in markdown, but not in MDX:

    console.log(1) // this is a paragraph in MDX!

The reason for that is so that you can nicely indent your components.

A different one is “autolinks”:

<svg:rect> and <admin@example.com> are links in markdown, but they crash xdm.
The reason is that they look a lot like JSX components, and we prefer being unambiguous.
If you want links, use [descriptive text](https://and-the-link-here.com).

HTML doesn’t work, because MDX has JSX instead (see next section).

And you must escape less than (`<`) and opening braces (`{`) like so: \< or \{.
```

More on this is
[documented here](https://github.com/micromark/mdx-state-machine#72-deviations-from-markdown).

### JSX

Most of JSX works.
Here’s some that looks a lot like HTML (but is JSX):

```js
<h1>Heading!</h1>

<abbr title="HyperText Markup Language">HTML</abbr> is a lovely language.

<section>
  And here is *markdown* in **JSX**!
</section>
```

You can also use components, but note that you must either define them locally
or pass them in later (see [§ MDX content][mdx-content]):

```js
<MyComponent id="123" />

Or access the `thisOne` component on the `myComponents` object: <myComponents.thisOne />

<Component
  open
  x={1}
  label={'this is a string, *not* markdown!'}
  icon={<Icon />}
/>
```

More on this is
[documented here](https://github.com/micromark/mdx-state-machine#73-deviations-from-jsx).

### ESM

To define things from within MDX, use ESM:

```js
import {External} from './some/place.js'

export const Local = props => <span style={{color: 'red'}} {...props} />

An <External /> component and <Local>a local component</Local>.
```

ESM can also be used for other things:

```js
import {MyChart} from './chart-component.js'
import data from './population.js'
export const pi = 3.14

<MyChart data={data} label={'Something with ' + pi} />
```

### Expressions

Braces can be used to embed JavaScript expressions in MDX:

```mdx
export const pi = 3.14

Two 🍰 is: {pi * 2}
```

Expressions can be empty or contain just a comment:

```mdx
{/* A comment! */}
```

## MDX content

All content (headings, paragraphs, etc) you write are exported as the default
export from a compiled MDX file as a component.

It’s possible to pass props in.
The special prop `components` is used to determine how to render components.
This includes both JSX and markdown syntax.
Say we have a `message.mdx` file:

```mdx
# Hello, *<Planet />*!

Remember when we first met in {props.year}?
```

This file could be imported from JavaScript and passed components like so:

```js
import Message from './message.mdx' // Assumes an integration is used to compile MDX -> JS.

<Message components={{Planet: () => 'Venus'}} year={1962} />
```

You can also change the things that come from markdown:

```js
<Message
  components={{
    // Map `h1` (`# heading`) to use `h2`s.
    h1: 'h2',
    // Rewrite `em`s (`*like so*`) to `i` with a red foreground color.
    em: (props) => <i style={{color: 'red'}} {...props} />,
    // Pass a layout (using the special `'wrapper'` key).
    wrapper: ({components, ...props}) => <main {...props} />,
    // Pass a component.
    Planet: () => 'Venus'
  }}
  year={1962}
/>
```

### Components

The following keys can be passed in `components`:

*   HTML equivalents for the things you write with markdown (such as `h1` for
    `# heading`)**†**
*   `wrapper`, which defines the layout (but local layout takes precedence)
*   `*` anything else that is a valid JavaScript identifier (`foo`,
    `Components`, `_`, `$x`, `a1`) for the things you write with JSX (like
    `<So />` or `<like.so />`, note that locally defined components take
    precedence)**‡**

**†** Normally, in markdown, those are: `a`, `blockquote`, `code`, `em`, `h1`,
`h2`, `h3`, `h4`, `h5`, `h6`, `hr`, `img`, `li`, `ol`, `p`, `pre`, `strong`, and
`ul`.
With [`remark-gfm`][gfm] ([see guide below](#github-flavored-markdown-gfm)), you
can also use: `del`, `table`, `tbody`, `td`, `th`, `thead`, and `tr`.
Other remark plugins that add support for new constructs and advertise that they
work with rehype, will also work with **xdm**.

**‡** The rules for whether a name in JSX (`x` in `<x>`) is a literal tag name
or not, are as follows:

*   If there’s a dot, it’s a member expression (`<a.b>` -> `h(a.b)`)
*   Otherwise, if the name is not a valid identifier, it’s a literal (`<a-b>` ->
    `h('a-b')`)
*   Otherwise, if it starts with a lowercase, it’s a literal (`<a>` -> `h('a')`)
*   Otherwise, it’s an identifier (`<A>` -> `h(A)`)

### Layout

Layouts are components that wrap the whole content.
They can be defined from within MDX using a default export:

```js
export default function Layout({children}) {
  return <main>{children}</main>;
}

All the things.
```

The layout can also be imported and *then* exported with an `export … from`:

```js
export {Layout as default} from './components.js'
```

The layout can also be passed as `components.wrapper` (but a local one takes
precedence).

## Integrations

### Bundlers

#### esbuild

Install `xdm` and use `xdm/esbuild.js`.
Add something along these lines to your `build` call:

```js
import xdm from 'xdm/esbuild.js'
import esbuild from 'esbuild'

await esbuild.build({
  entryPoints: ['index.mdx'],
  outfile: 'output.js',
  format: 'esm',
  plugins: [xdm({/* Options… */})]
})
```

esbuild takes care of turning modern JavaScript features into syntax that works
wherever you want it to.
No Babel needed.
See esbuild’s docs for more info.

`options` are the same as from [`compile`][compile] with the addition of:

###### `options.allowDangerousRemoteMdx`

Whether to allow importing from `http:` and `https:` URLs (`boolean`, default:
`false`).
See [§ Importing `.md` and `.mdx` files from the web in
esbuild][import-from-web].

> ⚠️ Note that this evaluates any JavaScript and MDX found over the wire!

#### Rollup

Install `xdm` and use `xdm/rollup.js`.
Add something along these lines to your `rollup.config.js`:

```js
import path from 'node:path'
import xdm from 'xdm/rollup.js'

export default {
  // …
  plugins: [
    // …
    xdm({/* Options… */})
  ]
}
```

If you use modern JavaScript features you might want to use Babel through
[`@rollup/plugin-babel`](https://github.com/rollup/plugins/tree/master/packages/babel)
to compile to code that works:

```js
// …
import {babel} from '@rollup/plugin-babel'

export default {
  // …
  plugins: [
    // …
    xdm({/* Options… */}),
    babel({
      // Also run on what used to be `.mdx` (but is now JS):
      extensions: ['.js', '.jsx', '.es6', '.es', '.mjs', '.mdx'],
      // Other options…
    })
  ]
}
```

Source maps are supported when [`SourceMapGenerator`][sm] is passed in.

`options` are the same as from [`compile`][compile], with the additions of:

###### `options.include`

###### `options.exclude`

List of [`picomatch`][pico] patterns to include and/or exclude
(`string`, `RegExp`, `(string|RegExp)[]`, default: `[]`).

#### Webpack

Install `xdm` and use `xdm/webpack.cjs`.
Add something along these lines to your `webpack.config.js`:

```js
module.exports = {
  module: {
    // …
    rules: [
      // …
      {test: /\.mdx$/, use: [{loader: 'xdm/webpack.cjs', options: {}}]}
    ]
  }
}
```

Source maps are supported when [`SourceMapGenerator`][sm] is passed in.

If you use modern JavaScript features you might want to use Babel through
[`babel-loader`](https://webpack.js.org/loaders/babel-loader/) to compile to
code that works:

```js
// …
use: [
  // Note that Webpack runs right-to-left: `xdm` is used first, then
  // `babel-loader`.
  {loader: 'babel-loader', options: {}},
  {loader: 'xdm/webpack.cjs', options: {}}
]
// …
```

Note that `webpack-cli` doesn’t support loaders in ESM directly or even
*indirectly*.
Because `xdm` itself is ESM, this means the `xdm/webpack.cjs` loader (even
though it’s CJS) doesn’t work with `webpack-cli` (it does work when using the
webpack API).
To use this loader with `webpack-cli`, set the `DISABLE_V8_COMPILE_CACHE=1`
environment variable.
See
[GH-11](https://github.com/wooorm/xdm/issues/11#issuecomment-785043772) for
details.

```sh
DISABLE_V8_COMPILE_CACHE=1 webpack
```

### Build systems

#### Snowpack

[Snowpack](https://www.snowpack.dev) uses [Rollup][] (for local files) which can
be extended.
Unfortunately, `snowpack.config.js` is currently, ironically, CommonJS.
So figuring out a way to `import('xdm/rollup.js')` and use it in Snowpack, is
left as an exercise to the reader.

#### Vite

[Vite](https://vitejs.dev) supports [Rollup][] plugins directly in `plugins` in
your `vite.config.js`.

#### WMR

[WMR](https://github.com/preactjs/wmr) supports [Rollup][] plugins directly by
[adding them to `plugins`](https://wmr.dev/docs/plugins/)
in `wmr.config.mjs`.

```js
import {defineConfig} from 'wmr'
import xdm from 'xdm/rollup.js'

export default defineConfig({
  plugins: [
    xdm({/* Options… */})
  ]
})
```

See [§ Preact](https://github.com/wooorm/xdm#preact) if you want to use Preact.

### Compilers

#### Babel

You should probably use webpack or Rollup instead of Babel directly as that
gives the neatest interface.
It is possible to use **xdm** in Babel and it’s fast, because it skips `xdm`
serialization and Babel parsing, if Babel is used anyway.

Babel does not support syntax extensions to its parser (it has “syntax” plugins
but those in fact turn certain flags on or off).
It does support setting a different parser.
Which in turn lets us choose whether to use the `xdm` or `@babel/parser`.

This Babel plugin, `plugin.js`:

```js
import path from 'node:path'
import parser from '@babel/parser'
import estreeToBabel from 'estree-to-babel'
import {compileSync} from 'xdm'

export function babelPluginSyntaxMdx() {
  // Tell Babel to use a different parser.
  return {parserOverride: babelParserWithMdx}
}

// A Babel parser that parses `.mdx` files with xdm and passes any other things
// through to the normal Babel parser.
function babelParserWithMdx(value, options) {
  if (
    options.sourceFilename &&
    path.extname(options.sourceFilename) === '.mdx'
  ) {
    // Babel does not support async parsers, unfortunately.
    return compileSync(
      {value, path: options.sourceFilename},
      // Tell xdm to return a Babel tree instead of serialized JS.
      {recmaPlugins: [recmaBabel]}
    ).result
  }

  return parser.parse(value, options)
}

// A “recma” plugin is a unified plugin that runs on the estree (used by xdm
// and much of the JS ecosystem but not Babel).
// This plugin defines `'estree-to-babel'` as the compiler, which means that
// the resulting Babel tree is given back by `compileSync`.
function recmaBabel() {
  Object.assign(this, {Compiler: estreeToBabel})
}
```

Can be used like so with the Babel API:

```js
import babel from '@babel/core'
import {babelPluginSyntaxMdx} from './plugin.js'

// Note that a filename must be set for our plugin to know it’s MDX instead of JS.
await babel.transformAsync(file, {filename: 'example.mdx', plugins: [babelPluginSyntaxMdx]})
```

### Site generators

#### Create React App (CRA)

Create a new app with [CRA](https://github.com/facebook/create-react-app) and
change directory to enter it:

```sh
npx create-react-app my-app
cd my-app
```

Install `xdm` as a dev dependency:

```sh
yarn add xdm --dev
```

Now we can add our MDX content.
Create an MDX file `Content.mdx` in the `src/` folder:

```mdx
export const Box = () => (
  <div style={{padding: 20, backgroundColor: 'tomato'}} />
)

# Hello, world!

This is **markdown** with <span style={{color: "red"}}>JSX</span>: MDX!

<Box />
```

To use that content in the app, replace the contents of `App.js` in the `src/`
folder with:

```js
/* eslint-disable import/no-webpack-loader-syntax */
import Content from '!xdm/webpack.cjs!./Content.mdx'

export default function App() {
  return <Content />
}
```

Done!
To start the development server run:

```sh
yarn start
```

#### Next

Next uses webpack.
Install `xdm` and extend
[Next’s config](https://nextjs.org/docs/api-reference/next.config.js/custom-webpack-config)
in a `next.config.js` file like so:

```js
module.exports = {
  // Support MDX files as pages:
  pageExtensions: ['mdx', 'tsx', 'ts', 'jsx', 'js'],
  // Support loading `.mdx`:
  webpack(config) {
    config.module.rules.push({
      test: /\.mdx$/,
      use: [{loader: 'xdm/webpack.cjs', options: {}}]
    })

    return config
  }
}
```

### Hyperscript implementations (frameworks)

#### React

Works out of the box.

> What about **React server components**?
>
> While they are currently alpha and not shipping soon, there is an
> [experimental demo](https://wooorm.com/server-components-mdx-demo/)
> combining **xdm** with RSC.

You can set `providerImportSource` to `'@mdx-js/react'` (which has to be
installed) to support context-based components passing.

```js
import {MDXProvider} from '@mdx-js/react'
import Post from './post.mdx' // Assumes an integration is used to compile MDX -> JS.

<MDXProvider components={{em: props => <i {...props} />}}>
  <Post />
</MDXProvider>
```

But the above can also be written without configuring and importing a provider:

```js
import Post from './post.mdx'

<Post components={{em: props => <i {...props} />}} />
```

#### Preact

Define a different import source in [options][compile]:

```js
compile(file, {jsxImportSource: 'preact'})
```

You can set `providerImportSource` to `'@mdx-js/preact'` (which has to be
installed) to support context-based components passing.
See React above for more information (but use `@mdx-js/preact`).

#### Svelte

Use [mdsvex][]!

#### Vue

Use Vue 3, which adds support for functional components and fragments, two
features heavily used in MDX.

Vue has a special way to compile JSX: **xdm** can’t do it but Babel can.
Tell `xdm` to keep the JSX:

```js
const jsx = String(await compile(file, {jsx: true}))
```

Then compile the JSX away with Babel and
[`@vue/babel-plugin-jsx`](https://github.com/vuejs/jsx-next/tree/dev/packages/babel-plugin-jsx):

```js
import babel from '@babel/core'

const js = (await babel.transformAsync(jsx, {plugins: ['@vue/babel-plugin-jsx']})).code
```

You are probably already using [webpack][] and/or [Rollup][] with Vue.
If not directly, then perhaps through something like Vue CLI.
In which case, see the above sections on these tools for how to use them, but
configure them as shown in this section to import `.mdx` files.

### Runtime libraries

#### Emotion

Define a different import source in [options][compile] at compile time:

```js
compile(file, {jsxImportSource: '@emotion/react'})
```

Otherwise, Emotion is React based, so see the React section for more info.

#### Theme UI

Theme UI is a React-specific library that requires using context to access its
effective components.
This can be done at the place where you’re using MDX content at runtime:

```js
import {base} from '@theme-ui/preset-base'
import {components, ThemeProvider} from 'theme-ui'
import Post from './post.mdx' // Assumes an integration is used to compile MDX -> JS.

<ThemeProvider theme={base}>
  <Post components={components} />
</ThemeProvider>
```

If using a `providerImportSource` set to `'@mdx-js/react'` while compiling,
Theme UI automatically injects its components into that context:

```js
import {base} from '@theme-ui/preset-base'
import {ThemeProvider} from 'theme-ui'
import Post from './post.mdx'

<ThemeProvider theme={base}>
  <Post />
</ThemeProvider>
```

Otherwise, Theme UI is Emotion and React based, so see their sections for more
info.

## Guides

### GitHub flavored markdown (GFM)

To support GFM (autolink literals, strikethrough, tables, and tasklists) use
[`remark-gfm`](https://github.com/remarkjs/remark-gfm).
Say we have an MDX file like this:

```mdx
# GFM

## Autolink literals

www.example.com, https://example.com, and contact@example.com.

## Strikethrough

~one~ or ~~two~~ tildes.

## Table

| a | b  |  c |  d  |
| - | :- | -: | :-: |

## Tasklist

* [ ] to do
* [x] done
```

Then do something like this:

```js
import {promises as fs} from 'node:fs'
import remarkGfm from 'remark-gfm'
import {compile} from 'xdm'

main()

async function main() {
  console.log(
    String(
      await compile(await fs.readFile('example.mdx'), {remarkPlugins: [remarkGfm]})
    )
  )
}
```

<details>
<summary>Show equivalent JSX</summary>

```js
<h1>GFM</h1>
<h2>Autolink literals</h2>
<p>
  <a href="http://www.example.com">www.example.com</a>,
  <a href="https://example.com">https://example.com</a>, and
  <a href="mailto:contact@example.com">contact@example.com</a>.
</p>
<h2>Strikethrough</h2>
<p>
  <del>one</del> or <del>two</del> tildes.
</p>
<h2>Table</h2>
<table>
  <thead>
    <tr>
      <th>a</th>
      <th align="left">b</th>
      <th align="right">c</th>
      <th align="center">d</th>
    </tr>
  </thead>
</table>
<h2>Tasklist</h2>
<ul className="contains-task-list">
  <li className="task-list-item">
    <input type="checkbox" disabled /> to do
  </li>
  <li className="task-list-item">
    <input type="checkbox" checked disabled /> done
  </li>
</ul>
```

</details>

### Syntax highlighting

There are two ways to accomplish syntax highlighting: at compile time or at
runtime.
Doing it at compile time means much less code is sent down the wire (syntax
highlighting needs a *lot* of code).
Doing it at runtime gives flexibility.

#### Syntax highlighting at compile time

Use either [`rehype-highlight`](https://github.com/rehypejs/rehype-highlight)
(`highlight.js`) or [`@mapbox/rehype-prism`](https://github.com/mapbox/rehype-prism)
(Prism) by doing something like this:

```js
import rehypeHighlight from 'rehype-highlight'
import {compile} from 'xdm'

main(`~~~js
console.log(1)
~~~`)

async function main(code) {
  console.log(
    String(await compile(code, {rehypePlugins: [rehypeHighlight]}))
  )
}
```

…you still need to load a relevant style sheet.

<details>
<summary>Show equivalent JSX</summary>

```js
<pre>
  <code className="hljs language-js">
    <span className="hljs-built_in">console</span>.log(
    <span className="hljs-number">1</span>)
  </code>
</pre>
```

</details>

#### Syntax highlighting at run time

Use for example
[`react-syntax-highlighter`](https://github.com/react-syntax-highlighter/react-syntax-highlighter),
by doing something like this:

```js
import SyntaxHighlighter from 'react-syntax-highlighter'
import Post from './example.mdx' // Assumes an integration is used to compile MDX -> JS.

<Post components={{code}} />

function code({className, ...props}) {
  const match = /language-(\w+)/.exec(className || '')
  return match
    ? <SyntaxHighlighter language={match[1]} PreTag="div" {...props} />
    : <code className={className} {...props} />
}
```

<details>
<summary>Show equivalent JSX</summary>

```js
<pre>
  <div
    className="language-js"
    style={{
      display: 'block',
      overflowX: 'auto',
      padding: '0.5em',
      background: '#F0F0F0',
      color: '#444'
    }}
  >
    <code style={{whiteSpace: 'pre'}}>
      <span>console.</span>
      <span style={{color: '#397300'}}>log</span>
      <span>(</span>
      <span style={{color: '#880000'}}>1</span>
      <span>)</span>
    </code>
  </div>
</pre>
```

</details>

#### Syntax highlighting with the `meta` field

Markdown supports a meta string for code:

````markdown
```js filename="index.js"
console.log(1)
```
````

This is a *hidden* part of markdown: it’s normally not rendered.
But as the above example shows, it’s a useful place to put some extra fields.

**xdm** doesn’t know whether you’re handling code as a component or what the
format of that meta string is, so it defaults to how markdown handles it: `meta`
is ignored.

The short answer is:
use [`remark-mdx-code-meta`](https://github.com/remarkjs/remark-mdx-code-meta),
it lets you type JSX attributes in the `meta` part and exposes them on the
`pre` component.

Or you can do it yourself, however you want, by writing a custom plugin to
interpret the `meta` field.
For example, it’s possible to pass that string as a prop by writing a rehype
plugin:

```js
function rehypeMetaAsAttribute() {
  return transform
}

function transform(tree) {
  visit(tree, 'element', onelement)
}

function onelement(node) {
  if (node.tagName === 'code' && node.data && node.data.meta) {
    node.properties.meta = node.data.meta
  }
}
```

This would yields the following JSX:

```jsx
<pre>
  <code class="language-js" meta='filename="index.js"'>
    console.log(1)
  </code>
</pre>
```

Note that the `meta` attribute is not valid HTML, so make sure to handle `code`
with a component.

The meta string in this example looks a lot like HTML attributes.
What if we wanted to parse that string and add each “attribute” as a prop?
Using the same rehype plugin as above, but with a different `onelement`
function, that can be achieved:

```js
const re = /\b([-\w]+)(?:=(?:"([^"]*)"|'([^']*)'|([^"'\s]+)))?/g

// …

function onelement(node) {
  let match

  if (node.tagName === 'code' && node.data && node.data.meta) {
    re.lastIndex = 0 // Reset regex.

    while ((match = re.exec(node.data.meta))) {
      node.properties[match[1]] = match[2] || match[3] || match[4] || ''
    }
  }
}
```

This would yields the following JSX:

```jsx
<pre>
  <code class="language-js" filename="index.js">
    console.log(1)
  </code>
</pre>
```

Note that the these added attributes are not valid HTML, so make sure to handle
`code` with a component.

### Math

Use
[`remark-math`](https://github.com/remarkjs/remark-math/tree/main/packages/remark-math)
and either
[`rehype-katex`](https://github.com/remarkjs/remark-math/tree/main/packages/rehype-katex)
(KaTeX) or
[`rehype-mathjax`](https://github.com/remarkjs/remark-math/tree/main/packages/rehype-mathjax)
(MathJax) by doing something like this:

```js
import rehypeKatex from 'rehype-katex'
import remarkMath from 'remark-math'
import {compile} from 'xdm'

main()

async function main() {
  console.log(
    String(
      // You only need one backslash in an MDX file but because this is JS wrapping it,
      // a double backslash is needed.
      await compile('# $\\sqrt{a^2 + b^2}$', {
        remarkPlugins: [remarkMath],
        rehypePlugins: [rehypeKatex]
      })
    )
  )
}
```

…you still need to load a KaTeX style sheet when using `rehype-katex`.

<details>
<summary>Show equivalent JSX</summary>

```js
<h1>
  <span className="math math-inline">
    <span className="katex">
      <span className="katex-mathml">
        <math xmlns="http://www.w3.org/1998/Math/MathML">…</math>
      </span>
      <span className="katex-html" aria-hidden="true">…</span>
    </span>
  </span>
</h1>
```

</details>

### Footnotes

Use
[`remark-footnotes`](https://github.com/remarkjs/remark-footnotes)
by doing something like this:

```js
import remarkFootnotes from 'remark-footnotes'
import {compile} from 'xdm'

main(`Hi[^1]

[^1]: World!`)

async function main(file) {
  console.log(String(await compile(file, {remarkPlugins: [remarkFootnotes]})))
}
```

<details>
<summary>Show equivalent JSX</summary>

```js
<p>
  Hi
  <a href="#fn1" className="footnote-ref" id="fnref1" role="doc-noteref">
    <sup>1</sup>
  </a>
</p>
<section className="footnotes" role="doc-endnotes">
  <hr />
  <ol>
    <li id="fn1" role="doc-endnote">
      World!
      <a href="#fnref1" className="footnote-back" role="doc-backlink">↩</a>
    </li>
  </ol>
</section>
```

</details>

### Frontmatter

Frontmatter, typically in YAML format, is frequently combined with markdown.
MDX comes with support for ESM (import/exports) which is a powerful dynamic
alternative.

Say we had this `post.mdx`:

```mdx
export const name = 'World'
export const title = 'Hi, ' + name + '!'

# {title}
```

Used like so:

```js
import * as Post from './post.mdx' // Assumes an integration is used to compile MDX -> JS.

console.log(Post.title) // Prints 'Hi, World!'
```

Still, you might prefer frontmatter because it lets you define data that can be
extracted from files *without* (or before) compiling:

Say our `post.mdx` with frontmatter looked like this:

```mdx
---
title: Hi, World!
---

# Hi, World!
```

Then without compiling or evaluating that file the metadata can be accessed like
so:

```js
import {promises as fs} from 'node:fs'
import yaml from 'js-yaml'

main()

async function main() {
  console.log(yaml.loadAll(await fs.readFile('example.mdx'))[0]) // Prints `{title: 'Hi, World!'}`
}
```

`xdm` doesn’t understand YAML frontmatter by default but can understand it
using [`remark-frontmatter`](https://github.com/remarkjs/remark-frontmatter):

```js
import {promises as fs} from 'node:fs'
import remarkFrontmatter from 'remark-frontmatter'
import {compile} from 'xdm'

main()

async function main() {
  console.log(
    await compile(await fs.readFile('example.mdx'), {
      remarkPlugins: [remarkFrontmatter]
    })
  )
}
```

Now it “works”: the frontmatter is ignored.
But it’s not available from *inside* the MDX.
What if we wanted to use frontmatter from inside the MDX file too?
Like so?

```mdx
---
title: Hi, World!
---

# {frontmatter.title}
```

That’s what
[`remark-mdx-frontmatter`](https://github.com/remcohaszing/remark-mdx-frontmatter)
does.

## Plugins

xdm has several extension points:

*   Components and a layout (wrapper) can be defined internally or passed at
    runtime (see [§ MDX content][mdx-content])
*   Plugins can hook into several stages of compilation ([remark
    plugins][remark-plugins], [rehype plugins][rehype-plugins], and the new
    recma plugins)

There are also a few of these extensions made specifically for MDX:

###### Components

None yet!

###### Plugins

*   [`rehype-mdx-title`](https://github.com/remcohaszing/rehype-mdx-title)
    — expose the page title as a string
*   [`remark-mdx-code-meta`](https://github.com/remcohaszing/remark-mdx-code-meta)
    — interpret the code `meta` field as JSX props
*   [`remark-mdx-images`](https://github.com/remcohaszing/remark-mdx-images)
    — change image sources to JavaScript imports
*   [`remark-mdx-frontmatter`](https://github.com/remcohaszing/remark-mdx-frontmatter)
    — change frontmatter (YAML) metadata to exports

## Types

This package is fully typed with [TypeScript](https://www.typescriptlang.org).

To enable types for imported `.mdx`, `.md`, etcetera files, first make sure
the TypeScript `JSX` namespace is typed (such as by importing the `react`
types), and then import `xdm/registry`.

```js
/**
 * @typedef {import('react')} */
 * @typedef {import('xdm/registry')} */
 */

import Post from './example.mdx'
// `Post` is now typed.
```

Alternatively, in TypeScript, do:

```ts
/// <reference types="react" />
/// <reference types="xdm/registry" />

import Post from './example.mdx'
// `Post` is now typed.
```

## Differences from `@mdx-js/mdx`

**API** (build):

*   Remove `skipExport` or `wrapExport` options
*   Add support for automatic JSX runtime
*   Add support for non-react classic runtime
*   Add support for source maps
*   Add `evaluate` instead of `runtime` package to eval MDX
*   Remove JSX from output (by default)
*   Default to automatic JSX runtime
*   No [GFM by default](#github-flavored-markdown-gfm)

**API** (run):

*   No providers by default
*   No runtime at all
*   `export`s work in `evaluate`
*   Add support for compiling import statements to dynamic import expressions
*   Add support for resolving import/export sources

**Input**:

*   ± same as `main` branch of `@mdx-js/mdx`
*   Fix JSX tags to prevent `<p><h1 /></p>`
*   Plain markdown can be loaded (`format: 'md'`)

**Output**:

*   No `isMDXContent` prop on the `MDXContent` component
*   Missing components throw instead of warn
*   Sandbox: when passing `components: {h1 = () => ...}` that component gets
    used for `# heading` but not for `<h1>heading</h1>`
*   Local components (including layouts) precede over given components
*   Remove support for passing `parent.child` combos (`ol.li`) for components
*   Remove support for passing `inlineCode` component (use `pre` and/or `code`
    instead)
*   Support for import and exports in `evaluate`
*   Fix a bug with encoding `"` in attributes

**Experiments**:

*   Add support for `import Content from './file.mdx'` in Node
*   Add support for `require('./file.mdx')` in Node
*   Add support `allowDangerousRemoteMdx` in esbuild to load MD(X) from the web

## Architecture

To understand what this project does, it’s very important to first understand
what unified does: please read through the
[`unifiedjs/unified`](https://github.com/unifiedjs/unified) readme (the part
until you hit the API section is required reading).

**xdm** is a unified pipeline — wrapped so that most folks don’t need to know
about unified:
[`core.js#L76-L102`](https://github.com/wooorm/xdm/blob/main/lib/core.js#L58-L84).
The processor goes through these steps:

1.  Parse MDX (serialized markdown with embedded JSX, ESM, and expressions)
    to mdast (markdown syntax tree)
2.  Transform through remark (markdown ecosystem)
3.  Transform mdast to hast (HTML syntax tree)
4.  Transform through rehype (HTML ecosystem)
5.  Transform hast to esast (JS syntax tree)
6.  Do the work needed to get a component
7.  Transform through recma (JS ecosystem)
8.  Serialize esast as JavaScript

The *input* is MDX (serialized markdown with embedded JSX, ESM, and
expressions).
The markdown is parsed with [`micromark`][micromark] and the embedded JS with
one of its extensions
[`micromark-extension-mdxjs`](https://github.com/micromark/micromark-extension-mdxjs)
(which in turn uses [acorn][]).
Then [`mdast-util-from-markdown`](https://github.com/syntax-tree/mdast-util-from-markdown)
and its extension
[`mdast-util-mdx`](https://github.com/syntax-tree/mdast-util-mdx) are used to
turn the results from the parser into a syntax tree:
[mdast](https://github.com/syntax-tree/mdast).

Markdown is closest to the source format.
This is where [remark plugins][remark-plugins] come in.
Typically, there shouldn’t be much going on here.
But perhaps you want to support GFM (tables and such) or frontmatter?
Then you can add a plugin here: `remark-gfm` or `remark-frontmatter`,
respectively.

After markdown, we go to [hast](https://github.com/syntax-tree/hast) (HTML).
This transformation is done by
[`mdast-util-to-hast`](https://github.com/syntax-tree/mdast-util-to-hast).
Wait, why, what does HTML have to do with it?
Part of the reason is that we care about HTML semantics: we want to know that
something is an `<a>`, not whether it’s a link with a resource (`[text](url)`)
or a reference to a defined link definition (`[text][id]\n\n[id]: url`).
So an HTML AST is *closer* to where we want to go.
Another reason is that there are many things folks need when they go MDX -> JS,
markdown -> HTML, or even folks who only process their HTML -> HTML: use cases
other than xdm.
By having a single AST in these cases and writing a plugin that works on that
AST, that plugin can supports *all* these use cases (for example,
[`rehype-highlight`](https://github.com/rehypejs/rehype-highlight)
for syntax highlighting or
[`rehype-katex`](https://github.com/remarkjs/remark-math/tree/main/packages/rehype-katex)
for math).
So, this is where [rehype plugins][rehype-plugins] come in: most of the plugins,
probably.

Then we go to JavaScript: [esast](https://github.com/syntax-tree/esast) (JS; an
AST which is compatible with estree but looks a bit more like other unist ASTs).
This transformation is done by
[`hast-util-to-estree`](https://github.com/syntax-tree/hast-util-to-estree).
This is a new ecosystem that does not have utilities or plugins yet.
But it’s where **xdm** does its thing: where it adds imports/exports, where it
compiles JSX away into `_jsx()` calls, and where it does the other cool things
that it provides.

Finally, The output is serialized JavaScript.
That final step is done by [astring](https://github.com/davidbonnet/astring), a
small and fast JS generator.

## Security

MDX is unsafe: it’s a programming language.
You might want to look into using `<iframe>`s with `sandbox`, but security is
hard, and that doesn’t seem to be 100%.
For Node, [vm2](https://github.com/patriksimek/vm2) sounds interesting.
But you should probably also sandbox the whole OS (Docker?), perform rate
limiting, and make sure processes can be killed when taking too long.

## Related

A lot of things are going on in `xdm`: parsing markdown to a syntax tree,
handling JavaScript (and JS) inside that markdown, converting to an HTML syntax
tree, converting *that* to a Js syntax tree, all the while running several
transforms, before finally serializing JavaScript.

Most of the work is done by:

*   [`micromark`][micromark]
    — Handles parsing of markdown (CommonMark)
*   [`acorn`][acorn]
    — Handles parsing of JS (ECMAScript)
*   [`unifiedjs.com`](https://unifiedjs.com)
    — Ties it all together

## License

[MIT][license] © [Titus Wormer][author], Compositor, and Vercel, Inc.

<!-- Definitions -->

[build-badge]: https://github.com/wooorm/xdm/workflows/main/badge.svg

[build]: https://github.com/wooorm/xdm/actions

[coverage-badge]: https://img.shields.io/codecov/c/github/wooorm/xdm.svg

[coverage]: https://codecov.io/github/wooorm/xdm

[downloads-badge]: https://img.shields.io/npm/dm/xdm.svg

[downloads]: https://www.npmjs.com/package/xdm

[size-badge]: https://img.shields.io/bundlephobia/minzip/xdm.svg

[size]: https://bundlephobia.com/result?p=xdm

[npm]: https://docs.npjs.com/cli/install

[yarn]: https://classic.yarnpkg.com/docs/cli/add/

[license]: license

[author]: https://wooorm.com

[buffer]: https://nodejs.org/api/buffer.html

[mdxc]: https://github.com/jamesknelson/mdxc

[mdxjs]: https://github.com/mdx-js/mdx

[mdsvex]: https://www.github.com/pngwn/mdsvex

[lit]: https://en.wikipedia.org/wiki/Literate_programming

[commonmark]: https://commonmark.org

[source-map]: https://github.com/mozilla/source-map

[vfile]: https://github.com/vfile/vfile

[remark-plugins]: https://github.com/remarkjs/remark/blob/main/doc/plugins.md#list-of-plugins

[rehype-plugins]: https://github.com/rehypejs/rehype/blob/main/doc/plugins.md#list-of-plugins

[gfm]: https://github.com/remarkjs/remark-gfm

[async-function]: https://developer.mozilla.org/docs/JavaScript/Reference/Global_Objects/AsyncFunction

[function]: https://developer.mozilla.org/docs/JavaScript/Reference/Global_Objects/Function

[compile]: #compilefile-options

[eval]: #evaluatefile-options

[integrations]: #integrations

[mdx-syntax]: #mdx-syntax

[mdx-content]: #mdx-content

[use]: #use

[format]: #optionsformat

[outputformat]: #optionsoutputformat

[baseurl]: #optionsbaseurl

[usedynamicimport]: #optionsusedynamicimport

[sm]: #optionssourcemapgenerator

[esbuild]: #esbuild

[rollup]: #rollup

[webpack]: #webpack

[caveats]: #caveats

[plugins]: #plugins

[micromark]: https://github.com/micromark/micromark

[acorn]: https://github.com/acornjs/acorn

[pico]: https://github.com/micromatch/picomatch#globbing-features

[lab]: #-lab

[import-from-web]: #importing-md-and-mdx-files-from-the-web-in-esbuild

[security]: #security
