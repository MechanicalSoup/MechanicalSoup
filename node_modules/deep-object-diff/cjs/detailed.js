"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _added = _interopRequireDefault(require("./added.js"));

var _deleted = _interopRequireDefault(require("./deleted.js"));

var _updated = _interopRequireDefault(require("./updated.js"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

const detailedDiff = (lhs, rhs) => ({
  added: (0, _added.default)(lhs, rhs),
  deleted: (0, _deleted.default)(lhs, rhs),
  updated: (0, _updated.default)(lhs, rhs)
});

var _default = detailedDiff;
exports.default = _default;