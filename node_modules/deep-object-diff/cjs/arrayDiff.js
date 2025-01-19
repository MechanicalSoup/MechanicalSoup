"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _utils = require("./utils.js");

const diff = (lhs, rhs) => {
  if (lhs === rhs) return {}; // equal return no diff

  if (!(0, _utils.isObject)(lhs) || !(0, _utils.isObject)(rhs)) return rhs; // return updated rhs

  const l = lhs;
  const r = rhs;
  const deletedValues = Object.keys(l).reduce((acc, key) => {
    return (0, _utils.hasOwnProperty)(r, key) ? acc : { ...acc,
      [key]: undefined
    };
  }, {});

  if ((0, _utils.isDate)(l) || (0, _utils.isDate)(r)) {
    if (l.valueOf() == r.valueOf()) return {};
    return r;
  }

  if (Array.isArray(r) && Array.isArray(l)) {
    const deletedValues = l.reduce((acc, item, index) => {
      return (0, _utils.hasOwnProperty)(r, index) ? acc.concat(item) : acc.concat(undefined);
    }, []);
    return r.reduce((acc, rightItem, index) => {
      if (!(0, _utils.hasOwnProperty)(deletedValues, index)) {
        return acc.concat(rightItem);
      }

      const leftItem = l[index];
      const difference = diff(rightItem, leftItem);

      if ((0, _utils.isObject)(difference) && (0, _utils.isEmpty)(difference) && !(0, _utils.isDate)(difference)) {
        delete acc[index];
        return acc; // return no diff
      }

      return acc.slice(0, index).concat(rightItem).concat(acc.slice(index + 1)); // return updated key
    }, deletedValues);
  }

  return Object.keys(r).reduce((acc, key) => {
    if (!(0, _utils.hasOwnProperty)(l, key)) return { ...acc,
      [key]: r[key]
    }; // return added r key

    const difference = diff(l[key], r[key]);
    if ((0, _utils.isObject)(difference) && (0, _utils.isEmpty)(difference) && !(0, _utils.isDate)(difference)) return acc; // return no diff

    return { ...acc,
      [key]: difference
    }; // return updated key
  }, deletedValues);
};

var _default = diff;
exports.default = _default;