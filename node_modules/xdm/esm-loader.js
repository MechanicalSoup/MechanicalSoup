import {createLoader} from './lib/integration/node.js'

const {getFormat, transformSource} = createLoader()

export {getFormat, transformSource, createLoader}
