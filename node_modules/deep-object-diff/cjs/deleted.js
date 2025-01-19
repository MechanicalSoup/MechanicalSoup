"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _utils = require("./utils.js");

const deletedDiff = (lhs, rhs) => {
  if (lhs === rhs || !(0, _utils.isObject)(lhs) || !(0, _utils.isObject)(rhs)) return {};
  return Object.keys(lhs).reduce((acc, key) => {
    if ((0, _utils.hasOwnProperty)(rhs, key)) {
      const difference = deletedDiff(lhs[key], rhs[key]);
      if ((0, _utils.isObject)(difference) && (0, _utils.isEmpty)(difference)) return acc;
      acc[key] = difference;
      return acc;
    }

    acc[key] = undefined;
    return acc;
  }, (0, _utils.makeObjectWithoutPrototype)());
};

var _default = deletedDiff;
exports.default = _default;