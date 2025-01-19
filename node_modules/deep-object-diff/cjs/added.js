"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _utils = require("./utils.js");

const addedDiff = (lhs, rhs) => {
  if (lhs === rhs || !(0, _utils.isObject)(lhs) || !(0, _utils.isObject)(rhs)) return {};
  return Object.keys(rhs).reduce((acc, key) => {
    if ((0, _utils.hasOwnProperty)(lhs, key)) {
      const difference = addedDiff(lhs[key], rhs[key]);
      if ((0, _utils.isObject)(difference) && (0, _utils.isEmpty)(difference)) return acc;
      acc[key] = difference;
      return acc;
    }

    acc[key] = rhs[key];
    return acc;
  }, (0, _utils.makeObjectWithoutPrototype)());
};

var _default = addedDiff;
exports.default = _default;