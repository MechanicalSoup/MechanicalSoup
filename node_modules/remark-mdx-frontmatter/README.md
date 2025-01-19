# remark-mdx-frontmatter

[![github actions][github actions badge]][github actions] [![npm][npm badge]][npm]
[![prettier][prettier badge]][prettier]

> A [remark][] plugin for converting frontmatter metadata into MDX exports

## Installation

This package depends on the AST output by [remark-frontmatter][]

```sh
npm install remark-frontmatter remark-mdx-frontmatter
```

## Usage

This remark plugin takes frontmatter content, and outputs it as JavaScript exports. Both YAML and
TOML frontmatter data are supported.

For example, given a file named `example.mdx` with the following contents:

```mdx
---
hello: frontmatter
---

Rest of document
```

The following script:

```js
import { readFileSync } from 'fs';

import remarkFrontmatter from 'remark-frontmatter';
import { remarkMdxFrontmatter } from 'remark-mdx-frontmatter';
import { compileSync } from 'xdm';

const { contents } = compileSync(readFileSync('example.mdx'), {
  jsx: true,
  remarkPlugins: [remarkFrontmatter, remarkMdxFrontmatter],
});
console.log(contents);
```

Roughly yields:

```jsx
export const hello = 'frontmatter';

export default function MDXContent() {
  return <p>Rest of document</p>;
}
```

### Options

#### `name`

By default, every frontmatter object key is turned into a JavaScript export. If `name` is specified,
the YAML content is exported as one single export using this name. This is useful if you wish to use
top-level frontmatter nodes other than objects, or if the frontmatter content contains keys which
aren’t valid JavaScript identifiers.

[github actions badge]:
  https://github.com/remcohaszing/remark-mdx-frontmatter/actions/workflows/ci.yml/badge.svg
[github actions]: https://github.com/remcohaszing/remark-mdx-frontmatter/actions/workflows/ci.yml
[npm badge]: https://img.shields.io/npm/v/remark-mdx-frontmatter
[npm]: https://www.npmjs.com/package/remark-mdx-frontmatter
[prettier badge]: https://img.shields.io/badge/code_style-prettier-ff69b4.svg
[prettier]: https://prettier.io
[remark]: https://remark.js.org
[remark-frontmatter]: https://github.com/remarkjs/remark-frontmatter
