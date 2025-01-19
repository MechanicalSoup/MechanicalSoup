"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _utils = require("./utils.js");

const updatedDiff = (lhs, rhs) => {
  if (lhs === rhs) return {};
  if (!(0, _utils.isObject)(lhs) || !(0, _utils.isObject)(rhs)) return rhs;

  if ((0, _utils.isDate)(lhs) || (0, _utils.isDate)(rhs)) {
    if (lhs.valueOf() == rhs.valueOf()) return {};
    return rhs;
  }

  return Object.keys(rhs).reduce((acc, key) => {
    if ((0, _utils.hasOwnProperty)(lhs, key)) {
      const difference = updatedDiff(lhs[key], rhs[key]); // If the difference is empty, and the lhs is an empty object or the rhs is not an empty object

      if ((0, _utils.isEmptyObject)(difference) && !(0, _utils.isDate)(difference) && ((0, _utils.isEmptyObject)(lhs[key]) || !(0, _utils.isEmptyObject)(rhs[key]))) return acc; // return no diff

      acc[key] = difference;
      return acc;
    }

    return acc;
  }, (0, _utils.makeObjectWithoutPrototype)());
};

var _default = updatedDiff;
exports.default = _default;