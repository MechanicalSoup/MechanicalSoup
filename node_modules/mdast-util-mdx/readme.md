# mdast-util-mdx

[![Build][build-badge]][build]
[![Coverage][coverage-badge]][coverage]
[![Downloads][downloads-badge]][downloads]
[![Size][size-badge]][size]
[![Sponsors][sponsors-badge]][collective]
[![Backers][backers-badge]][collective]
[![Chat][chat-badge]][chat]

Extension for [`mdast-util-from-markdown`][from-markdown] and/or
[`mdast-util-to-markdown`][to-markdown] to support MDX (or MDX.js) in
**[mdast][]**.
When parsing (`from-markdown`), must be combined with either
[`micromark-extension-mdx`][mdx] or [`micromark-extension-mdxjs`][mdxjs].

## When to use this

Use this if you’re dealing with the AST manually and want to support all of MDX.
You can also use the extensions separately:

*   [`mdast-util-mdx-expression`](https://github.com/syntax-tree/mdast-util-mdx-expression)
    — support MDX (or MDX.js) expressions
*   [`mdast-util-mdx-jsx`](https://github.com/syntax-tree/mdast-util-mdx-jsx)
    — support MDX (or MDX.js) JSX
*   [`mdast-util-mdxjs-esm`](https://github.com/syntax-tree/mdast-util-mdxjs-esm)
    — support MDX.js ESM

## Install

This package is [ESM only](https://gist.github.com/sindresorhus/a39789f98801d908bbc7ff3ecc99d99c):
Node 12+ is needed to use it and it must be `import`ed instead of `require`d.

[npm][]:

```sh
npm install mdast-util-mdx
```

## Use

Say we have the following file, `example.mdx`:

```markdown
import Box from "place"

Here’s an expression:

{
  1 + 1 /* } */
}

Which you can also put inline: {1+1}.

<Box>
  <SmallerBox>
    - Lists, which can be indented.
  </SmallerBox>
</Box>
```

And our script, `example.js`, looks as follows:

```js
import fs from 'node:fs'
import {fromMarkdown} from 'mdast-util-from-markdown'
import {toMarkdown} from 'mdast-util-to-markdown'
import {mdxjs} from 'micromark-extension-mdxjs'
import {mdxFromMarkdown, mdxToMarkdown} from 'mdast-util-mdx'

const doc = fs.readFileSync('example.mdx')

const tree = fromMarkdown(doc, {
  extensions: [mdxjs()],
  mdastExtensions: [mdxFromMarkdown]
})

console.log(tree)

const out = toMarkdown(tree, {extensions: [mdxToMarkdown]})

console.log(out)
```

Now, running `node example` yields (positional info removed for brevity):

```js
{
  type: 'root',
  children: [
    {
      type: 'mdxjsEsm',
      value: 'import Box from "place"',
      data: {
        estree: {
          type: 'Program',
          body: [
            {
              type: 'ImportDeclaration',
              specifiers: [
                {
                  type: 'ImportDefaultSpecifier',
                  local: {type: 'Identifier', name: 'Box'}
                }
              ],
              source: {type: 'Literal', value: 'place', raw: '"place"'}
            }
          ],
          sourceType: 'module'
        }
      }
    },
    {
      type: 'paragraph',
      children: [{type: 'text', value: 'Here’s an expression:'}]
    },
    {
      type: 'mdxFlowExpression',
      value: '\n1 + 1 /* } */\n',
      data: {
        estree: {
          type: 'Program',
          body: [
            {
              type: 'ExpressionStatement',
              expression: {
                type: 'BinaryExpression',
                left: {type: 'Literal', value: 1, raw: '1'},
                operator: '+',
                right: {type: 'Literal', value: 1, raw: '1'}
              }
            }
          ],
          sourceType: 'module'
        }
      }
    },
    {
      type: 'paragraph',
      children: [
        {type: 'text', value: 'Which you can also put inline: '},
        {
          type: 'mdxTextExpression',
          value: '1+1',
          data: {
            estree: {
              type: 'Program',
              body: [
                {
                  type: 'ExpressionStatement',
                  expression: {
                    type: 'BinaryExpression',
                    left: {type: 'Literal', value: 1, raw: '1'},
                    operator: '+',
                    right: {type: 'Literal', value: 1, raw: '1'}
                  }
                }
              ],
              sourceType: 'module'
            }
          }
        },
        {type: 'text', value: '.'}
      ]
    },
    {
      type: 'mdxJsxFlowElement',
      name: 'Box',
      attributes: [],
      children: [
        {
          type: 'mdxJsxFlowElement',
          name: 'SmallerBox',
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
                    {
                      type: 'paragraph',
                      children: [
                        {type: 'text', value: 'Lists, which can be indented.'}
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

```markdown
import Box from "place"

Here’s an expression:

{
  1 + 1 /* } */
}

Which you can also put inline: {1+1}.

<Box>
  <SmallerBox>
    *   Lists, which can be indented.
  </SmallerBox>
</Box>
```

## API

This package exports the following identifier: `mdxFromMarkdown`,
`mdxToMarkdown`.
There is no default export.

### `mdxFromMarkdown`

### `mdxToMarkdown`

Support MDX (or MDX.js).
The exports are respectively an extension for
[`mdast-util-from-markdown`][from-markdown] and
[`mdast-util-to-markdown`][to-markdown].

There are no options.

## Related

*   [`remarkjs/remark`][remark]
    — markdown processor powered by plugins
*   [`remarkjs/remark-mdx`][remark-mdx]
    — remark plugin to support MDX (or MDX.js)
*   [`micromark/micromark`][micromark]
    — the smallest commonmark-compliant markdown parser that exists
*   [`micromark/micromark-extension-mdx`][mdx]
    — micromark extension to parse MDX
*   [`micromark/micromark-extension-mdxjs`][mdxjs]
    — micromark extension to parse MDX.js
*   [`syntax-tree/mdast-util-from-markdown`][from-markdown]
    — mdast parser using `micromark` to create mdast from markdown
*   [`syntax-tree/mdast-util-to-markdown`][to-markdown]
    — mdast serializer to create markdown from mdast

## Contribute

See [`contributing.md` in `syntax-tree/.github`][contributing] for ways to get
started.
See [`support.md`][support] for ways to get help.

This project has a [code of conduct][coc].
By interacting with this repository, organization, or community you agree to
abide by its terms.

## License

[MIT][license] © [Titus Wormer][author]

<!-- Definitions -->

[build-badge]: https://github.com/syntax-tree/mdast-util-mdx/workflows/main/badge.svg

[build]: https://github.com/syntax-tree/mdast-util-mdx/actions

[coverage-badge]: https://img.shields.io/codecov/c/github/syntax-tree/mdast-util-mdx.svg

[coverage]: https://codecov.io/github/syntax-tree/mdast-util-mdx

[downloads-badge]: https://img.shields.io/npm/dm/mdast-util-mdx.svg

[downloads]: https://www.npmjs.com/package/mdast-util-mdx

[size-badge]: https://img.shields.io/bundlephobia/minzip/mdast-util-mdx.svg

[size]: https://bundlephobia.com/result?p=mdast-util-mdx

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

[mdx]: https://github.com/micromark/micromark-extension-mdx

[mdxjs]: https://github.com/micromark/micromark-extension-mdxjs

[remark-mdx]: https://github.com/mdx-js/mdx/tree/next/packages/remark-mdx
