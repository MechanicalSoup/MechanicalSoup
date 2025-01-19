import { isObject, hasOwnProperty } from './utils.js';

const getLargerArray = (l, r) => l.length > r.length ? l : r;

const preserve = (diff, left, right) => {

  if (!isObject(diff)) return diff;

  return Object.keys(diff).reduce((acc, key) => {

    const leftArray = left[key];
    const rightArray = right[key];

    if (Array.isArray(leftArray) && Array.isArray(rightArray)) {
      const array = [...getLargerArray(leftArray, rightArray)];
      return {
        ...acc,
        [key]: array.reduce((acc2, item, index) => {
          if (hasOwnProperty(diff[key], index)) {
            acc2[index] = preserve(diff[key][index], leftArray[index], rightArray[index]); // diff recurse and check for nested arrays
            return acc2;
          }

          delete acc2[index]; // no diff aka empty
          return acc2;
        }, array)
      };
    }

    return {
      ...acc,
      [key]: diff[key]
    };
  }, {});
};

export default preserve;
