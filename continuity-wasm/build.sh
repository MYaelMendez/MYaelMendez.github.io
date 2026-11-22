#!/usr/bin/env bash
# Build continuity-core wasm. The standalone MSVC Rust on PATH lacks the wasm
# std; the rustup-managed toolchain has it. Put that bin first and clean stale
# artifacts compiled by the other rustc (otherwise E0514).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
RT="$HOME/.rustup/toolchains/stable-x86_64-pc-windows-msvc/bin"
export PATH="$RT:$PATH"
cd "$HERE"
cargo clean
wasm-pack build --target web --release --out-dir dist
echo "built: $(sha256sum dist/continuity_core_bg.wasm)"
