module.exports = {
  extends: "eslint:recommended",
  parserOptions: {
    sourceType: "module",
    babelOptions: {
      cwd: __dirname
    }
  },
  env: {
    node: true,
    es6: true,
    "jest/globals": true,
  },
  parser: "@babel/eslint-parser",
  plugins: ["jest"],
  rules: {
    "import/no-extraneous-dependencies": 0,
  },
};
