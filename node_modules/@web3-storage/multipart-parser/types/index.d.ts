export function streamMultipart(body: any, boundary: any): AsyncGenerator<any, void, unknown>;
/**
 *
 * @param {ReadableStream<Uint8Array>} body
 * @param {string} boundary
 * @returns {AsyncIterable<FilePart>}
 */
export function iterateMultipart(body: ReadableStream<Uint8Array>, boundary: string): AsyncIterable<FilePart>;
export type FilePart = {
    name: string;
    filename?: string;
    contentType?: string;
    data: Uint8Array;
};
//# sourceMappingURL=index.d.ts.map