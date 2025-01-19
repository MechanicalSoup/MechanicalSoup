<div align="center">
  <h1>deep-object-diff</h1>

  ❄️

  Deep diff two JavaScript Objects
</div>

<hr />

[![Build Status](https://github.com/mattphillips/deep-object-diff/actions/workflows/ci.yaml/badge.svg)](https://github.com/mattphillips/deep-object-diff/actions/workflows/ci.yaml)
[![Code coverage](https://codecov.io/gh/mattphillips/deep-object-diff/branch/main/graph/badge.svg?token=EwnXzDGW3x)](https://codecov.io/gh/mattphillips/deep-object-diff)
[![version](https://img.shields.io/npm/v/deep-object-diff.svg?style=flat-square)](https://www.npmjs.com/package/deep-object-diff)
[![downloads](https://img.shields.io/npm/dm/deep-object-diff.svg?style=flat-square)](http://npm-stat.com/charts.html?package=deep-object-diff&from=2016-11-23)
[![MIT License](https://img.shields.io/npm/l/deep-object-diff.svg?style=flat-square)](https://github.com/mattphillips/deep-object-diff/blob/master/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

A small library that can deep diff two JavaScript Objects, including nested structures of arrays and objects.

## Installation
`yarn add deep-object-diff`

`npm i --save deep-object-diff`

## Functions available:
 - [`diff(originalObj, updatedObj)`](#diff)
 returns the difference of the original and updated objects

 - [`addedDiff(original, updatedObj)`](#addeddiff)
 returns only the values added to the updated object

 - [`deletedDiff(original, updatedObj)`](#deleteddiff)
 returns only the values deleted in the updated object

 - [`updatedDiff(original, updatedObj)`](#updateddiff)
 returns only the values that have been changed in the updated object

 - [`detailedDiff(original, updatedObj)`](#detaileddiff)
 returns an object with the added, deleted and updated differences

## Importing

``` js
import { diff, addedDiff, deletedDiff, updatedDiff, detailedDiff } from 'deep-object-diff';
```

## Usage:

### `diff`:
```js
const lhs = {
  foo: {
    bar: {
      a: ['a', 'b'],
      b: 2,
      c: ['x', 'y'],
      e: 100 // deleted
    }
  },
  buzz: 'world'
};

const rhs = {
  foo: {
    bar: {
      a: ['a'], // index 1 ('b')  deleted
      b: 2, // unchanged
      c: ['x', 'y', 'z'], // 'z' added
      d: 'Hello, world!' // added
    }
  },
  buzz: 'fizz' // updated
};

console.log(diff(lhs, rhs)); // =>
/*
{
  foo: {
    bar: {
      a: {
        '1': undefined
      },
      c: {
        '2': 'z'
      },
      d: 'Hello, world!',
      e: undefined
    }
  },
  buzz: 'fizz'
}
*/
```

### `addedDiff`:
```js
const lhs = {
  foo: {
    bar: {
      a: ['a', 'b'],
      b: 2,
      c: ['x', 'y'],
      e: 100 // deleted
    }
  },
  buzz: 'world'
};

const rhs = {
  foo: {
    bar: {
      a: ['a'], // index 1 ('b')  deleted
      b: 2, // unchanged
      c: ['x', 'y', 'z'], // 'z' added
      d: 'Hello, world!' // added
    }
  },
  buzz: 'fizz' // updated
};

console.log(addedDiff(lhs, rhs));

/*
{
  foo: {
    bar: {
      c: {
        '2': 'z'
      },
      d: 'Hello, world!'
    }
  }
}
*/
```

### `deletedDiff`:
```js
const lhs = {
  foo: {
    bar: {
      a: ['a', 'b'],
      b: 2,
      c: ['x', 'y'],
      e: 100 // deleted
    }
  },
  buzz: 'world'
};

const rhs = {
  foo: {
    bar: {
      a: ['a'], // index 1 ('b')  deleted
      b: 2, // unchanged
      c: ['x', 'y', 'z'], // 'z' added
      d: 'Hello, world!' // added
    }
  },
  buzz: 'fizz' // updated
};

console.log(deletedDiff(lhs, rhs));

/*
{
  foo: {
    bar: {
      a: {
        '1': undefined
      },
      e: undefined
    }
  }
}
*/
```

### `updatedDiff`:
```js
const lhs = {
  foo: {
    bar: {
      a: ['a', 'b'],
      b: 2,
      c: ['x', 'y'],
      e: 100 // deleted
    }
  },
  buzz: 'world'
};

const rhs = {
  foo: {
    bar: {
      a: ['a'], // index 1 ('b')  deleted
      b: 2, // unchanged
      c: ['x', 'y', 'z'], // 'z' added
      d: 'Hello, world!' // added
    }
  },
  buzz: 'fizz' // updated
};

console.log(updatedDiff(lhs, rhs));

/*
{
  buzz: 'fizz'
}
*/
```

### `detailedDiff`:
```js
const lhs = {
  foo: {
    bar: {
      a: ['a', 'b'],
      b: 2,
      c: ['x', 'y'],
      e: 100 // deleted
    }
  },
  buzz: 'world'
};

const rhs = {
  foo: {
    bar: {
      a: ['a'], // index 1 ('b')  deleted
      b: 2, // unchanged
      c: ['x', 'y', 'z'], // 'z' added
      d: 'Hello, world!' // added
    }
  },
  buzz: 'fizz' // updated
};

console.log(detailedDiff(lhs, rhs));

/*
{
  added: {
    foo: {
      bar: {
        c: {
          '2': 'z'
        },
        d: 'Hello, world!'
      }
    }
  },
  deleted: {
    foo: {
      bar: {
        a: {
          '1': undefined
        },
        e: undefined
      }
    }
  },
  updated: {
    buzz: 'fizz'
  }
}
*/
```


## License

MIT
