export const isDate = d => d instanceof Date;
export const isEmpty = o => Object.keys(o).length === 0;
export const isObject = o => o != null && typeof o === 'object';
export const hasOwnProperty = (o, ...args) => Object.prototype.hasOwnProperty.call(o, ...args)
export const isEmptyObject = (o) => isObject(o) && isEmpty(o);
export const makeObjectWithoutPrototype = () => Object.create(null);
