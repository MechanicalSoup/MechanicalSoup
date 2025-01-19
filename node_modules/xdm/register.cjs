'use strict'

const runtime = require('react/jsx-runtime')
const register = require('./lib/integration/require.cjs')

register({...runtime})
