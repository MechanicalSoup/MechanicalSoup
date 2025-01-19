#!/usr/bin/env node
const fs = require('fs')
const globby = require('globby')
const sortPackageJson = require('.')

const isCheckFlag = (argument) => argument === '--check' || argument === '-c'

const cliArguments = process.argv.slice(2)
const isCheck = cliArguments.some(isCheckFlag)

const patterns = cliArguments.filter((argument) => !isCheckFlag(argument))

if (!patterns.length) {
  patterns[0] = 'package.json'
}

const files = globby.sync(patterns)

if (files.length === 0) {
  console.log('No matching files.')
  process.exit(1)
}

let notSortedFiles = 0

files.forEach((file) => {
  const packageJson = fs.readFileSync(file, 'utf8')
  const sorted = sortPackageJson(packageJson)

  if (sorted !== packageJson) {
    if (isCheck) {
      notSortedFiles++
      console.log(file)
    } else {
      fs.writeFileSync(file, sorted, 'utf8')
      console.log(`${file} is sorted!`)
    }
  }
})

if (isCheck) {
  console.log()
  if (notSortedFiles) {
    console.log(
      notSortedFiles === 1
        ? `${notSortedFiles} of ${files.length} matched file is not sorted.`
        : `${notSortedFiles} of ${files.length} matched files are not sorted.`,
    )
  } else {
    console.log(
      files.length === 1
        ? `${files.length} matched file is sorted.`
        : `${files.length} matched files are sorted.`,
    )
  }
  process.exit(notSortedFiles)
}
