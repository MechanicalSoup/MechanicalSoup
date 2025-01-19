# modern-ahocorasick

> Forked from `https://github.com/BrunoRB/ahocorasick` and make it modern! Thanks to the author(`BrunoRB`) of `ahocorasick`

Implementation of the Aho-Corasick string searching algorithm, as described in the paper "Efficient string matching: an aid to bibliographic search".

this pkg has `cjs` and `esm` format, and have `.d.ts` file.

## Install

```sh
<npm/yarn/pnpm> i modern-ahocorasick
```

## Usage

```ts
// cjs
const AhoCorasick = require('modern-ahocorasick');
// esm
import AhoCorasick from 'modern-ahocorasick'

const ac = new AhoCorasick(['keyword1', 'keyword2', 'etc']);
const results = ac.search('should find keyword1 at position 19 and keyword2 at position 47.');

// [ [ 19, [ 'keyword1' ] ], [ 47, [ 'keyword2' ] ] ]
```

## Visualization

See <https://brunorb.github.io/ahocorasick/visualization.html> for an interactive visualization of the algorithm.

## License

[The MIT License](LICENSE)
