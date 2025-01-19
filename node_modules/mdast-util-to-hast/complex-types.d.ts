import {Literal} from 'hast'

export interface Raw extends Literal {
  type: 'raw'
}

declare module 'hast' {
  interface RootContentMap {
    raw: Raw
  }

  interface ElementContentMap {
    raw: Raw
  }
}
