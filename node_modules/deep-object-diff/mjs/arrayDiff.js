import { isDate, isEmpty, isObject, hasOwnProperty } from './utils.js';

const diff = (lhs, rhs) => {
  if (lhs === rhs) return {}; // equal return no diff

  if (!isObject(lhs) || !isObject(rhs)) return rhs; // return updated rhs

  const l = lhs;
  const r = rhs;

  const deletedValues = Object.keys(l).reduce((acc, key) => {
    return hasOwnProperty(r, key) ? acc : { ...acc, [key]: undefined };
  }, {});

  if (isDate(l) || isDate(r)) {
    if (l.valueOf() == r.valueOf()) return {};
    return r;
  }

  if (Array.isArray(r) && Array.isArray(l)) {
    const deletedValues = l.reduce((acc, item, index) => {
      return hasOwnProperty(r, index) ? acc.concat(item) : acc.concat(undefined);
    }, []);

    return r.reduce((acc, rightItem, index) => {
      if (!hasOwnProperty(deletedValues, index)) {
        return acc.concat(rightItem);
      }

      const leftItem = l[index];
      const difference = diff(rightItem, leftItem);

      if (isObject(difference) && isEmpty(difference) && !isDate(difference)) {
        delete acc[index];
        return acc; // return no diff
      }

      return acc.slice(0, index).concat(rightItem).concat(acc.slice(index + 1)); // return updated key
    }, deletedValues);
  }

  return Object.keys(r).reduce((acc, key) => {
    if (!hasOwnProperty(l, key)) return { ...acc, [key]: r[key] }; // return added r key

    const difference = diff(l[key], r[key]);

    if (isObject(difference) && isEmpty(difference) && !isDate(difference)) return acc; // return no diff

    return { ...acc, [key]: difference }; // return updated key
  }, deletedValues);
};

export default diff;
