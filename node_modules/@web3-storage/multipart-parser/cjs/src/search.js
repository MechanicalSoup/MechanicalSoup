'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

var utils = require('./utils.js');

function coerce(a) {
  if (a instanceof Uint8Array) {
    return index => a[index];
  }
  return a;
}
function jsmemcmp(buf1, pos1, buf2, pos2, len) {
  const fn1 = coerce(buf1);
  const fn2 = coerce(buf2);
  for (let i = 0; i < len; ++i) {
    if (fn1(pos1 + i) !== fn2(pos2 + i)) {
      return false;
    }
  }
  return true;
}
function createOccurenceTable(s) {
  const table = new Array(256).fill(s.length);
  if (s.length > 1) {
    for (let i = 0; i < s.length - 1; i++) {
      table[s[i]] = s.length - 1 - i;
    }
  }
  return table;
}
const MATCH = Symbol('Match');
class StreamSearch {
  constructor(needle) {
    this._lookbehind = new Uint8Array();
    if (typeof needle === 'string') {
      this._needle = needle = utils.stringToArray(needle);
    } else {
      this._needle = needle;
    }
    this._lastChar = needle[needle.length - 1];
    this._occ = createOccurenceTable(needle);
  }
  feed(chunk) {
    let pos = 0;
    let tokens;
    const allTokens = [];
    while (pos !== chunk.length) {
      ;
      [pos, ...tokens] = this._feed(chunk, pos);
      allTokens.push(...tokens);
    }
    return allTokens;
  }
  end() {
    const tail = this._lookbehind;
    this._lookbehind = new Uint8Array();
    return tail;
  }
  _feed(data, bufPos) {
    const tokens = [];
    let pos = -this._lookbehind.length;
    if (pos < 0) {
      while (pos < 0 && pos <= data.length - this._needle.length) {
        const ch = this._charAt(data, pos + this._needle.length - 1);
        if (ch === this._lastChar && this._memcmp(data, pos, this._needle.length - 1)) {
          if (pos > -this._lookbehind.length) {
            tokens.push(this._lookbehind.slice(0, this._lookbehind.length + pos));
          }
          tokens.push(MATCH);
          this._lookbehind = new Uint8Array();
          return [
            pos + this._needle.length,
            ...tokens
          ];
        } else {
          pos += this._occ[ch];
        }
      }
      if (pos < 0) {
        while (pos < 0 && !this._memcmp(data, pos, data.length - pos)) {
          pos++;
        }
      }
      if (pos >= 0) {
        tokens.push(this._lookbehind);
        this._lookbehind = new Uint8Array();
      } else {
        const bytesToCutOff = this._lookbehind.length + pos;
        if (bytesToCutOff > 0) {
          tokens.push(this._lookbehind.slice(0, bytesToCutOff));
          this._lookbehind = this._lookbehind.slice(bytesToCutOff);
        }
        this._lookbehind = Uint8Array.from(new Array(this._lookbehind.length + data.length), (_, i) => this._charAt(data, i - this._lookbehind.length));
        return [
          data.length,
          ...tokens
        ];
      }
    }
    pos += bufPos;
    while (pos <= data.length - this._needle.length) {
      const ch = data[pos + this._needle.length - 1];
      if (ch === this._lastChar && data[pos] === this._needle[0] && jsmemcmp(this._needle, 0, data, pos, this._needle.length - 1)) {
        if (pos > bufPos) {
          tokens.push(data.slice(bufPos, pos));
        }
        tokens.push(MATCH);
        return [
          pos + this._needle.length,
          ...tokens
        ];
      } else {
        pos += this._occ[ch];
      }
    }
    if (pos < data.length) {
      while (pos < data.length && (data[pos] !== this._needle[0] || !jsmemcmp(data, pos, this._needle, 0, data.length - pos))) {
        ++pos;
      }
      if (pos < data.length) {
        this._lookbehind = data.slice(pos);
      }
    }
    if (pos > 0) {
      tokens.push(data.slice(bufPos, pos < data.length ? pos : data.length));
    }
    return [
      data.length,
      ...tokens
    ];
  }
  _charAt(data, pos) {
    if (pos < 0) {
      return this._lookbehind[this._lookbehind.length + pos];
    }
    return data[pos];
  }
  _memcmp(data, pos, len) {
    return jsmemcmp(this._charAt.bind(this, data), pos, this._needle, 0, len);
  }
}
class ReadableStreamSearch {
  constructor(needle, _readableStream) {
    this._readableStream = _readableStream;
    this._search = new StreamSearch(needle);
  }
  async *[Symbol.asyncIterator]() {
    const reader = this._readableStream.getReader();
    try {
      while (true) {
        const result = await reader.read();
        if (result.done) {
          break;
        }
        yield* this._search.feed(result.value);
      }
      const tail = this._search.end();
      if (tail.length) {
        yield tail;
      }
    } finally {
      reader.releaseLock();
    }
  }
}
const EOQ = Symbol('End of Queue');
class QueueableStreamSearch {
  constructor(needle) {
    this._chunksQueue = [];
    this._closed = false;
    this._search = new StreamSearch(needle);
  }
  push(...chunks) {
    if (this._closed) {
      throw new Error('cannot call push after close');
    }
    this._chunksQueue.push(...chunks);
    if (this._notify) {
      this._notify();
    }
  }
  close() {
    if (this._closed) {
      throw new Error('close was already called');
    }
    this._closed = true;
    this._chunksQueue.push(EOQ);
    if (this._notify) {
      this._notify();
    }
  }
  async *[Symbol.asyncIterator]() {
    while (true) {
      let chunk;
      while (!(chunk = this._chunksQueue.shift())) {
        await new Promise(resolve => this._notify = resolve);
        this._notify = undefined;
      }
      if (chunk === EOQ) {
        break;
      }
      yield* this._search.feed(chunk);
    }
    const tail = this._search.end();
    if (tail.length) {
      yield tail;
    }
  }
}
function splitChunks(chunks, needle) {
  const search = new StreamSearch(needle);
  const outchunks = [[]];
  for (const chunk of chunks) {
    for (const token of search.feed(chunk)) {
      if (token === MATCH) {
        outchunks.push([]);
      } else {
        outchunks[outchunks.length - 1].push(token);
      }
    }
  }
  const end = search.end();
  outchunks[outchunks.length - 1].push(end);
  return outchunks.map(chunks => utils.mergeArrays(...chunks));
}
function split(buf, needle) {
  return splitChunks([buf], needle);
}
async function* chunksIterator(iter) {
  let chunks = [];
  for await (const value of iter) {
    if (value === MATCH) {
      yield chunks;
      chunks = [];
    } else {
      chunks.push(value);
    }
  }
  yield chunks;
}
async function* stringIterator(iter) {
  for await (const chunk of chunksIterator(iter)) {
    yield chunk.map(utils.arrayToString).join('');
  }
}
async function allStrings(iter) {
  const segments = [];
  for await (const value of stringIterator(iter)) {
    segments.push(value);
  }
  return segments;
}
async function* arrayIterator(iter) {
  for await (const chunk of chunksIterator(iter)) {
    yield utils.mergeArrays(...chunk);
  }
}

exports.MATCH = MATCH;
exports.QueueableStreamSearch = QueueableStreamSearch;
exports.ReadableStreamSearch = ReadableStreamSearch;
exports.StreamSearch = StreamSearch;
exports.allStrings = allStrings;
exports.arrayIterator = arrayIterator;
exports.chunksIterator = chunksIterator;
exports.split = split;
exports.splitChunks = splitChunks;
exports.stringIterator = stringIterator;
