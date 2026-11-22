/* tslint:disable */
/* eslint-disable */

/**
 * Real SHA-256 over bytes — no placeholder hash.
 */
export function canon_sha256(bytes: Uint8Array | number[]): string;

/**
 * wasm-bindgen: rewrite INPUTS and re-derive. Same inputs → same receipt.
 */
export function derive(state_json: string, inputs_json: string): string;

export function doctor(): string;

/**
 * Two derivations, byte-compared. A receipt is evidence only after both match.
 */
export function grade(state_json: string, inputs_json: string): string;

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
    readonly memory: WebAssembly.Memory;
    readonly canon_sha256: (a: number, b: number, c: number) => void;
    readonly derive: (a: number, b: number, c: number, d: number, e: number) => void;
    readonly doctor: (a: number) => void;
    readonly grade: (a: number, b: number, c: number, d: number, e: number) => void;
    readonly __wbindgen_externrefs: WebAssembly.Table;
    readonly __wbindgen_add_to_stack_pointer: (a: number) => number;
    readonly __wbindgen_export: (a: number, b: number) => number;
    readonly __wbindgen_export2: (a: number, b: number, c: number) => void;
    readonly __wbindgen_export3: (a: number, b: number, c: number, d: number) => number;
    readonly __wbindgen_start: () => void;
}

export type SyncInitInput = BufferSource | WebAssembly.Module;

/**
 * Instantiates the given `module`, which can either be bytes or
 * a precompiled `WebAssembly.Module`.
 *
 * @param {{ module: SyncInitInput }} module - Passing `SyncInitInput` directly is deprecated.
 *
 * @returns {InitOutput}
 */
export function initSync(module: { module: SyncInitInput } | SyncInitInput): InitOutput;

/**
 * If `module_or_path` is {RequestInfo} or {URL}, makes a request and
 * for everything else, calls `WebAssembly.instantiate` directly.
 *
 * @param {{ module_or_path: InitInput | Promise<InitInput> }} module_or_path - Passing `InitInput` directly is deprecated.
 *
 * @returns {Promise<InitOutput>}
 */
export default function __wbg_init (module_or_path?: { module_or_path: InitInput | Promise<InitInput> } | InitInput | Promise<InitInput>): Promise<InitOutput>;
