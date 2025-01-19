"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.makeObjectWithoutPrototype = exports.isObject = exports.isEmptyObject = exports.isEmpty = exports.isDate = exports.hasOwnProperty = void 0;

const isDate = d => d instanceof Date;

exports.isDate = isDate;

const isEmpty = o => Object.keys(o).length === 0;

exports.isEmpty = isEmpty;

const isObject = o => o != null && typeof o === 'object';

exports.isObject = isObject;

const hasOwnProperty = (o, ...args) => Object.prototype.hasOwnProperty.call(o, ...args);

exports.hasOwnProperty = hasOwnProperty;

const isEmptyObject = o => isObject(o) && isEmpty(o);

exports.isEmptyObject = isEmptyObject;

const makeObjectWithoutPrototype = () => Object.create(null);

exports.makeObjectWithoutPrototype = makeObjectWithoutPrototype;