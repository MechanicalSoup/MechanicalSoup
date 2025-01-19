# mdast-util-mdx-jsx

[![Build][build-badge]][build]
[![Coverage][coverage-badge]][coverage]
[![Downloads][downloads-badge]][downloads]
[![Size][size-badge]][size]
[![Sponsors][sponsors-badge]][collective]
[![Backers][backers-badge]][collective]
[![Chat][chat-badge]][chat]

Extension for [`mdast-util-from-markdown`][from-markdown] and/or
[`mdast-util-to-markdown`][to-markdown] to support MDX (or MDX.js) JSX.
When parsing (`from-markdown`), must be combined with
[`micromark-extension-mdx-jsx`][extension].

This utility handles parsing and serializing.
See [`micromark-extension-mdx-jsx`][extension] for how the syntax works.

## When to use this

Use [`mdast-util-mdx`][mdast-util-mdx] if you want all of MDX / MDX.js.
Use this otherwise.

## Install

This package is [ESM only](https://gist.github.com/sindresorhus/a39789f98801d908bbc7ff3ecc99d99c):
Node 12+ is needed to use it and it must be `import`ed instead of `require`d.

[npm][]:

```sh
npm install mdast-util-mdx-jsx
```

## Use

Say we have an MDX.js file, `example.mdx`:

```mdx
<Box>
  - a list
</Box>

<MyComponent {...props} />

<abbr title="Hypertext Markup Language">HTML</abbr> is a lovely language.
```

And our module, `example.js`, looks as follows:

```js
import fs from 'node:fs'
import * as acorn from 'acorn'
import {fromMarkdown} from 'mdast-util-from-markdown'
import {toMarkdown} from 'mdast-util-to-markdown'
import {mdxJsx} from 'micromark-extension-mdx-jsx'
import {mdxJsxFromMarkdown, mdxJsxToMarkdown} from 'mdast-util-mdx-jsx'

const doc = fs.readFileSync('example.mdx')

const tree = fromMarkdown(doc, {
  extensions: [mdxJsx({acorn: acorn, addResult: true})],
  mdastExtensions: [mdxJsxFromMarkdown]
})

console.log(tree)

const out = toMarkdown(tree, {extensions: [mdxJsxToMarkdown]})

console.log(out)
```

Now, running `node example` yields (positional info removed for brevity):

```js
{
  type: 'root',
  children: [
    {
      type: 'mdxJsxFlowElement',
      name: 'Box',
      attributes: [],
      children: [
        {
          type: 'list',
          ordered: false,
          start: null,
          spread: false,
          children: [
            {
              type: 'listItem',
              spread: false,
              checked: null,
              children: [
                {type: 'paragraph', children: [{type: 'text', value: 'a list'}]}
              ]
            }
          ]
        }
      ]
    },
    {
      type: 'mdxJsxFlowElement',
      name: 'MyComponent',
      attributes: [
        {
          type: 'mdxJsxExpressionAttribute',
          value: '...props',
          data: {
            estree: {
              type: 'Program',
              body: [
                {
                  type: 'ExpressionStatement',
                  expression: {
                    type: 'ObjectExpression',
                    properties: [
                      {
                        type: 'SpreadElement',
                        argument: {type: 'Identifier', name: 'props'}
                      }
                    ]
                  }
                }
              ],
              sourceType: 'module'
            }
          }
        }
      ],
      children: []
    },
    {
      type: 'paragraph',
      children: [
        {
          type: 'mdxJsxTextElement',
          name: 'abbr',
          attributes: [
            {
              type: 'mdxJsxAttribute',
              name: 'title',
              value: 'Hypertext Markup Language'
            }
          ],
          children: [{type: 'text', value: 'HTML'}]
        },
        {type: 'text', value: ' is a lovely language.'}
      ]
    }
  ]
}
```

```markdown
<Box>
  *   a list
</Box>

<MyComponent {...props}/>

<abbr title="Hypertext Markup Language">HTML</abbr> is a lovely language.
```

## API

### `mdxJsxFromMarkdown`

### `mdxJsxToMarkdown`

Support MDX (or MDX.js) JSX.
The exports are extensions, respectively for
[`mdast-util-from-markdown`][from-markdown] and
[`mdast-util-to-markdown`][to-markdown].

When using the [syntax extension][extension] with `addResult`, nodes will have a
`data.estree` field set to an [ESTree][].

There are no options, but passing [`options.quote`][quote] to
`mdast-util-to-markdown` is honored for attributes.

this extension configures [`mdast-util-to-markdown`][to-markdown] with
`fences: true` and `resourceLink: true` too, do not overwrite them!

## Syntax tree

The following interfaces are added to **[mdast][]** by this utility.

### Nodes

#### `MDXJsxFlowElement`

```idl
interface MDXJsxFlowElement <: Parent {
  type: "mdxJsxFlowElement"
}

MDXJsxFlowElement includes MDXJsxElement
```

**MDXJsxFlowElement** (**[Parent][dfn-parent]**) represents JSX in flow (block).
It can be used where **[flow][dfn-content-flow]** content is expected.
It includes the mixin **[MDXJsxElement][dfn-mixin-mdx-jsx-element]**.

For example, the following markdown:

```markdown
<w x="y">
  z
</w>
```

Yields:

```js
{
  type: 'mdxJsxFlowElement',
  name: 'w',
  attributes: [{type: 'mdxJsxAttribute', name: 'x', value: 'y'}],
  children: [{type: 'paragraph', children: [{type: 'text', value: 'z'}]}]
}
```

#### `MDXJsxTextElement`

```idl
interface MDXJsxTextElement <: Parent {
  type: "mdxJsxTextElement"
}

MDXJsxTextElement includes MDXJsxElement
```

**MDXJsxTextElement** (**[Parent][dfn-parent]**) represents JSX in text (span,
inline).
It can be used where **[phrasing][dfn-content-phrasing]** content is
expected.
It includes the mixin **[MDXJsxElement][dfn-mixin-mdx-jsx-element]**.

For example, the following markdown:

```markdown
a <b c>d</b> e.
```

Yields:

```js
{
  type: 'mdxJsxTextElement',
  name: 'b',
  attributes: [{type: 'mdxJsxAttribute', name: 'c', value: null}],
  children: [{type: 'text', value: 'd'}]
}
```

### Mixin

### `MDXJsxElement`

```idl
interface mixin MDXJsxElement {
  name: string?
  attributes: [MDXJsxExpressionAttribute | MDXJsxAttribute]
}

interface MDXJsxExpressionAttribute <: Literal {
  type: "mdxJsxExpressionAttribute"
}

interface MDXJsxAttribute <: Node {
  type: "mdxJsxAttribute"
  name: string
  value: MDXJsxAttributeValueExpression | string?
}

interface MDXJsxAttributeValueExpression <: Literal {
  type: "mdxJsxAttributeValueExpression"
}
```

**MDXJsxElement** represents a JSX element.

The `name` field can be present and represents an identifier.
Without `name`, the element represents a fragment, in which case no attributes
must be present.

The `attributes` field represents information associated with the node.
The value of the `attributes` field is a list of **MDXJsxExpressionAttribute**
and **MDXJsxAttribute** nodes.

**MDXJsxExpressionAttribute** represents an expression (typically in a
programming language) that when evaluated results in multiple attributes.

**MDXJsxAttribute** represents a single attribute.
The `name` field must be present.
The `value` field can be present, in which case it is either a string (a static
value) or an expression (typically in a programming language) that when
evaluated results in an attribute value.

### Content model

#### `FlowContent` (MDX JSX)

```idl
type MDXJsxFlowContent = MDXJsxFlowElement | FlowContent
```

#### `PhrasingContent` (MDX JSX)

```idl
type MDXJsxPhrasingContent = MDXJsxTextElement | PhrasingContent
```

## Related

*   [`remarkjs/remark`][remark]
    — markdown processor powered by plugins
*   [`remarkjs/remark-mdx`][remark-mdx]
    — remark plugin to support MDX
*   [`syntax-tree/mdast-util-from-markdown`][from-markdown]
    — mdast parser using `micromark` to create mdast from markdown
*   [`syntax-tree/mdast-util-to-markdown`][to-markdown]
    — mdast serializer to create markdown from mdast
*   [`syntax-tree/mdast-util-mdx`][mdast-util-mdx]
    — mdast utility to support all of MDX
*   [`micromark/micromark`][micromark]
    — the smallest commonmark-compliant markdown parser that exists
*   [`micromark/micromark-extension-mdx-jsx`][extension]
    — micromark extension to parse JSX

## Contribute

See [`contributing.md` in `syntax-tree/.github`][contributing] for ways to get
started.
See [`support.md`][support] for ways to get help.

This project has a [code of conduct][coc].
By interacting with this repository, organization, or community you agree to
abide by its terms.

## License

[MIT][license] © [Titus Wormer][author]

[build-badge]: https://github.com/syntax-tree/mdast-util-mdx-jsx/workflows/main/badge.svg

[build]: https://github.com/syntax-tree/mdast-util-mdx-jsx/actions

[coverage-badge]: https://img.shields.io/codecov/c/github/syntax-tree/mdast-util-mdx-jsx.svg

[coverage]: https://codecov.io/github/syntax-tree/mdast-util-mdx-jsx

[downloads-badge]: https://img.shields.io/npm/dm/mdast-util-mdx-jsx.svg

[downloads]: https://www.npmjs.com/package/mdast-util-mdx-jsx

[size-badge]: https://img.shields.io/bundlephobia/minzip/mdast-util-mdx-jsx.svg

[size]: https://bundlephobia.com/result?p=mdast-util-mdx-jsx

[sponsors-badge]: https://opencollective.com/unified/sponsors/badge.svg

[backers-badge]: https://opencollective.com/unified/backers/badge.svg

[collective]: https://opencollective.com/unified

[chat-badge]: https://img.shields.io/badge/chat-discussions-success.svg

[chat]: https://github.com/syntax-tree/unist/discussions

[npm]: https://docs.npmjs.com/cli/install

[license]: license

[author]: https://wooorm.com

[contributing]: https://github.com/syntax-tree/.github/blob/HEAD/contributing.md

[support]: https://github.com/syntax-tree/.github/blob/HEAD/support.md

[coc]: https://github.com/syntax-tree/.github/blob/HEAD/code-of-conduct.md

[mdast]: https://github.com/syntax-tree/mdast

[remark]: https://github.com/remarkjs/remark

[from-markdown]: https://github.com/syntax-tree/mdast-util-from-markdown

[to-markdown]: https://github.com/syntax-tree/mdast-util-to-markdown

[micromark]: https://github.com/micromark/micromark

[extension]: https://github.com/micromark/micromark-extension-mdxjs-esm

[mdast-util-mdx]: https://github.com/syntax-tree/mdast-util-mdx

[quote]: https://github.com/syntax-tree/mdast-util-to-markdown#optionsquote

[estree]: https://github.com/estree/estree

[dfn-parent]: https://github.com/syntax-tree/mdast#parent

[dfn-content-flow]: #flowcontent-mdx-jsx

[dfn-content-phrasing]: #phrasingcontent-mdx-jsx

[dfn-mixin-mdx-jsx-element]: #mdxjsxelement

[remark-mdx]: https://github.com/mdx-js/mdx/tree/main/packages/remark-mdx
