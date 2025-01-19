export const MATCH: unique symbol;
export class QueueableStreamSearch {
    constructor(needle: any);
    _chunksQueue: any[];
    _closed: boolean;
    _search: StreamSearch;
    push(...chunks: any[]): void;
    close(): void;
    _notify: ((value: any) => void) | undefined;
    [Symbol.asyncIterator](): AsyncGenerator<any, void, undefined>;
}
export class ReadableStreamSearch {
    constructor(needle: any, _readableStream: any);
    _readableStream: any;
    _search: StreamSearch;
    [Symbol.asyncIterator](): AsyncGenerator<any, void, undefined>;
}
export class StreamSearch {
    constructor(needle: any);
    _lookbehind: Uint8Array;
    _needle: any;
    _lastChar: any;
    _occ: any[];
    feed(chunk: any): any[];
    end(): Uint8Array;
    _feed(data: any, bufPos: any): any[];
    _charAt(data: any, pos: any): any;
    _memcmp(data: any, pos: any, len: any): boolean;
}
export function allStrings(iter: any): Promise<string[]>;
export function arrayIterator(iter: any): AsyncGenerator<Uint8Array, void, unknown>;
export function chunksIterator(iter: any): AsyncGenerator<any[], void, unknown>;
export function split(buf: any, needle: any): Uint8Array[];
export function splitChunks(chunks: any, needle: any): Uint8Array[];
export function stringIterator(iter: any): AsyncGenerator<string, void, unknown>;
//# sourceMappingURL=search.d.ts.map