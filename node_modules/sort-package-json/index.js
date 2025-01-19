const sortObjectKeys = require('sort-object-keys')
const detectIndent = require('detect-indent')
const detectNewline = require('detect-newline').graceful
const gitHooks = require('git-hooks-list')
const isPlainObject = require('is-plain-obj')

const hasOwnProperty = (object, property) =>
  Object.prototype.hasOwnProperty.call(object, property)
const pipe =
  (fns) =>
  (x, ...args) =>
    fns.reduce((result, fn) => fn(result, ...args), x)
const onArray = (fn) => (x) => Array.isArray(x) ? fn(x) : x
const onStringArray = (fn) => (x) =>
  Array.isArray(x) && x.every((item) => typeof item === 'string') ? fn(x) : x
const uniq = onStringArray((xs) => xs.filter((x, i) => i === xs.indexOf(x)))
const sortArray = onStringArray((array) => [...array].sort())
const uniqAndSortArray = pipe([uniq, sortArray])
const onObject =
  (fn) =>
  (x, ...args) =>
    isPlainObject(x) ? fn(x, ...args) : x
const sortObjectBy = (comparator, deep) => {
  const over = onObject((object) => {
    object = sortObjectKeys(object, comparator)
    if (deep) {
      for (const [key, value] of Object.entries(object)) {
        object[key] = over(value)
      }
    }
    return object
  })

  return over
}
const sortObject = sortObjectBy()
const sortURLObject = sortObjectBy(['type', 'url'])
const sortPeopleObject = sortObjectBy(['name', 'email', 'url'])
const sortDirectories = sortObjectBy([
  'lib',
  'bin',
  'man',
  'doc',
  'example',
  'test',
])
const overProperty =
  (property, over) =>
  (object, ...args) =>
    hasOwnProperty(object, property)
      ? Object.assign(object, { [property]: over(object[property], ...args) })
      : object
const sortGitHooks = sortObjectBy(gitHooks)

// https://github.com/eslint/eslint/blob/acc0e47572a9390292b4e313b4a4bf360d236358/conf/config-schema.js
const eslintBaseConfigProperties = [
  // `files` and `excludedFiles` are only on `overrides[]`
  // for easier sort `overrides[]`,
  // add them to here, so we don't need sort `overrides[]` twice
  'files',
  'excludedFiles',
  // baseConfig
  'env',
  'parser',
  'parserOptions',
  'settings',
  'plugins',
  'extends',
  'rules',
  'overrides',
  'globals',
  'processor',
  'noInlineConfig',
  'reportUnusedDisableDirectives',
]
const sortEslintConfig = onObject(
  pipe([
    sortObjectBy(eslintBaseConfigProperties),
    overProperty('env', sortObject),
    overProperty('globals', sortObject),
    overProperty(
      'overrides',
      onArray((overrides) => overrides.map(sortEslintConfig)),
    ),
    overProperty('parserOptions', sortObject),
    overProperty(
      'rules',
      sortObjectBy(
        (rule1, rule2) =>
          rule1.split('/').length - rule2.split('/').length ||
          rule1.localeCompare(rule2),
      ),
    ),
    overProperty('settings', sortObject),
  ]),
)
const sortVSCodeBadgeObject = sortObjectBy(['description', 'url', 'href'])

const sortPrettierConfig = onObject(
  pipe([
    // sort keys alphabetically, but put `overrides` at bottom
    (config) =>
      sortObjectKeys(config, [
        ...Object.keys(config)
          .filter((key) => key !== 'overrides')
          .sort(),
        'overrides',
      ]),
    // if `config.overrides` exists
    overProperty(
      'overrides',
      // and `config.overrides` is an array
      onArray((overrides) =>
        overrides.map(
          pipe([
            // sort `config.overrides[]` alphabetically
            sortObject,
            // sort `config.overrides[].options` alphabetically
            overProperty('options', sortObject),
          ]),
        ),
      ),
    ),
  ]),
)

const sortVolta = sortObjectBy(['node', 'npm', 'yarn'])

// See https://docs.npmjs.com/misc/scripts
const defaultNpmScripts = new Set([
  'install',
  'pack',
  'prepare',
  'publish',
  'restart',
  'shrinkwrap',
  'start',
  'stop',
  'test',
  'uninstall',
  'version',
])

const hasDevDependency = (dependency, packageJson) => {
  return (
    'devDependencies' in packageJson &&
    !!packageJson.devDependencies[dependency]
  )
}

const sortScripts = onObject((scripts, packageJson) => {
  const names = Object.keys(scripts)
  const prefixable = new Set()

  const keys = names.map((name) => {
    const omitted = name.replace(/^(?:pre|post)/, '')
    if (defaultNpmScripts.has(omitted) || names.includes(omitted)) {
      prefixable.add(omitted)
      return omitted
    }
    return name
  })

  if (!hasDevDependency('npm-run-all', packageJson)) {
    keys.sort()
  }

  const order = keys.reduce(
    (order, key) =>
      order.concat(
        prefixable.has(key) ? [`pre${key}`, key, `post${key}`] : [key],
      ),
    [],
  )

  return sortObjectKeys(scripts, order)
})

// fields marked `vscode` are for `Visual Studio Code extension manifest` only
// https://code.visualstudio.com/api/references/extension-manifest
// Supported fields:
// publisher, displayName, categories, galleryBanner, preview, contributes,
// activationEvents, badges, markdown, qna, extensionPack,
// extensionDependencies, icon

// field.key{string}: field name
// field.over{function}: sort field subKey
const fields = [
  { key: '$schema' },
  { key: 'name' },
  /* vscode */ { key: 'displayName' },
  { key: 'version' },
  { key: 'private' },
  { key: 'description' },
  /* vscode */ { key: 'categories', over: uniq },
  { key: 'keywords', over: uniq },
  { key: 'homepage' },
  { key: 'bugs', over: sortObjectBy(['url', 'email']) },
  { key: 'repository', over: sortURLObject },
  { key: 'funding', over: sortURLObject },
  { key: 'license', over: sortURLObject },
  /* vscode */ { key: 'qna' },
  { key: 'author', over: sortPeopleObject },
  {
    key: 'maintainers',
    over: onArray((maintainers) => maintainers.map(sortPeopleObject)),
  },
  {
    key: 'contributors',
    over: onArray((contributors) => contributors.map(sortPeopleObject)),
  },
  /* vscode */ { key: 'publisher' },
  { key: 'sideEffects' },
  { key: 'type' },
  { key: 'imports' },
  { key: 'exports' },
  { key: 'main' },
  { key: 'svelte' },
  { key: 'umd:main' },
  { key: 'jsdelivr' },
  { key: 'unpkg' },
  { key: 'module' },
  { key: 'source' },
  { key: 'jsnext:main' },
  { key: 'browser' },
  { key: 'react-native' },
  { key: 'types' },
  { key: 'typesVersions' },
  { key: 'typings' },
  { key: 'style' },
  { key: 'example' },
  { key: 'examplestyle' },
  { key: 'assets' },
  { key: 'bin', over: sortObject },
  { key: 'man' },
  { key: 'directories', over: sortDirectories },
  { key: 'files', over: uniq },
  { key: 'workspaces' },
  // node-pre-gyp https://www.npmjs.com/package/node-pre-gyp#1-add-new-entries-to-your-packagejson
  {
    key: 'binary',
    over: sortObjectBy([
      'module_name',
      'module_path',
      'remote_path',
      'package_name',
      'host',
    ]),
  },
  { key: 'scripts', over: sortScripts },
  { key: 'betterScripts', over: sortScripts },
  /* vscode */ { key: 'contributes', over: sortObject },
  /* vscode */ { key: 'activationEvents', over: uniq },
  { key: 'husky', over: overProperty('hooks', sortGitHooks) },
  { key: 'simple-git-hooks', over: sortGitHooks },
  { key: 'pre-commit' },
  { key: 'commitlint', over: sortObject },
  { key: 'lint-staged' },
  { key: 'config', over: sortObject },
  { key: 'nodemonConfig', over: sortObject },
  { key: 'browserify', over: sortObject },
  { key: 'babel', over: sortObject },
  { key: 'browserslist' },
  { key: 'xo', over: sortObject },
  { key: 'prettier', over: sortPrettierConfig },
  { key: 'eslintConfig', over: sortEslintConfig },
  { key: 'eslintIgnore' },
  { key: 'npmpkgjsonlint', over: sortObject },
  { key: 'npmPackageJsonLintConfig', over: sortObject },
  { key: 'npmpackagejsonlint', over: sortObject },
  { key: 'release', over: sortObject },
  { key: 'remarkConfig', over: sortObject },
  { key: 'stylelint' },
  { key: 'ava', over: sortObject },
  { key: 'jest', over: sortObject },
  { key: 'mocha', over: sortObject },
  { key: 'nyc', over: sortObject },
  { key: 'c8', over: sortObject },
  { key: 'tap', over: sortObject },
  { key: 'resolutions', over: sortObject },
  { key: 'dependencies', over: sortObject },
  { key: 'devDependencies', over: sortObject },
  { key: 'dependenciesMeta', over: sortObjectBy(undefined, true) },
  { key: 'peerDependencies', over: sortObject },
  // TODO: only sort depth = 2
  { key: 'peerDependenciesMeta', over: sortObjectBy(undefined, true) },
  { key: 'optionalDependencies', over: sortObject },
  { key: 'bundledDependencies', over: uniqAndSortArray },
  { key: 'bundleDependencies', over: uniqAndSortArray },
  /* vscode */ { key: 'extensionPack', over: uniqAndSortArray },
  /* vscode */ { key: 'extensionDependencies', over: uniqAndSortArray },
  { key: 'flat' },
  { key: 'packageManager' },
  { key: 'engines', over: sortObject },
  { key: 'engineStrict', over: sortObject },
  { key: 'volta', over: sortVolta },
  { key: 'languageName' },
  { key: 'os' },
  { key: 'cpu' },
  { key: 'preferGlobal', over: sortObject },
  { key: 'publishConfig', over: sortObject },
  /* vscode */ { key: 'icon' },
  /* vscode */ {
    key: 'badges',
    over: onArray((badge) => badge.map(sortVSCodeBadgeObject)),
  },
  /* vscode */ { key: 'galleryBanner', over: sortObject },
  /* vscode */ { key: 'preview' },
  /* vscode */ { key: 'markdown' },
]

const defaultSortOrder = fields.map(({ key }) => key)
const overFields = pipe(
  fields.reduce((fns, { key, over }) => {
    if (over) {
      fns.push(overProperty(key, over))
    }
    return fns
  }, []),
)

function editStringJSON(json, over) {
  if (typeof json === 'string') {
    const { indent } = detectIndent(json)
    const endCharacters = json.slice(-1) === '\n' ? '\n' : ''
    const newline = detectNewline(json)
    json = JSON.parse(json)

    let result = JSON.stringify(over(json), null, indent) + endCharacters
    if (newline === '\r\n') {
      result = result.replace(/\n/g, newline)
    }
    return result
  }

  return over(json)
}

const isPrivateKey = (key) => key[0] === '_'
const partition = (array, predicate) =>
  array.reduce(
    (result, value) => {
      result[predicate(value) ? 0 : 1].push(value)
      return result
    },
    [[], []],
  )
function sortPackageJson(jsonIsh, options = {}) {
  return editStringJSON(
    jsonIsh,
    onObject((json) => {
      let sortOrder = options.sortOrder ? options.sortOrder : defaultSortOrder

      if (Array.isArray(sortOrder)) {
        const keys = Object.keys(json)
        const [privateKeys, publicKeys] = partition(keys, isPrivateKey)
        sortOrder = [
          ...sortOrder,
          ...defaultSortOrder,
          ...publicKeys.sort(),
          ...privateKeys.sort(),
        ]
      }

      return overFields(sortObjectKeys(json, sortOrder), json)
    }),
  )
}

module.exports = sortPackageJson
module.exports.sortPackageJson = sortPackageJson
module.exports.sortOrder = defaultSortOrder
module.exports.default = sortPackageJson
