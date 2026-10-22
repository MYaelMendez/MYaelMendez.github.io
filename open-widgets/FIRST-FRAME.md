# First 9:16 MoW Garden frame above origin

Continuity checkpoint: 2026-10-20. Requested scope: put a separate first widget frame at the top of root `index.html`, pushing existing content down without changing origin.

## Implementation

- `index.html`: one marked, normal-flow mount immediately after `<body>`. It contains a responsive 9:16 frame (maximum width 420px), an original-origin anchor, and a standalone-widget fallback link. All new styling is inline on added elements. No new parent script or generic CSS selectors.
- `open-widgets/first-frame.html`: independent first MoW Garden scene with native drawers, selectable widgets, and per-widget local nesting state. Its scrollable interior keeps content reachable when drawers expand or text is enlarged. No API, email, publishing, synchronization, or authentication is introduced.
- The iframe uses `sandbox="allow-scripts"` without same-origin, parent navigation, popup, form, or storage allowances. The child has no parent access code; its CSP disallows network connections.
- This is a standalone first-scene preview, not the complete four-scene v0.1 runtime or its backend. PR #26 remains independent. The existing OpenAI Site is untouched.

## Preservation evidence

Original index blob: `c218c350ebdaddb5ad636e8a4ae99b36e072d506`.
Mount commit: `ea5682990377ca4ae4367e28d491cd833380062e`.
GitHub comparison against its parent reports `index.html`: **13 lines added, 0 removed**. The only change is the marked block between `<body>` and the original `<canvas id="grid">`.
Frame implementation commit: `140db8748b09f2013d5c9b184d8aa8726d16e66e`.
The locally tested frame matches remote blob `312094d0b69b5e0881b6ead94227444707e37dab` byte-for-byte.

## Executed checks

Node syntax check passed for the child script. Chromium DOM tests passed at 390x844, 320x700, 844x390 and 1440x1000: 9:16 frame ratio, normal-flow placement above a baseline marker, no page-level horizontal overflow, opening drawers, widget selection, per-widget nesting-state restoration, keyboard toggling, and sandbox denial of parent DOM/storage access. Mobile preview was visually inspected.

**Test boundary:** tests loaded a local layout fixture with sandboxed `srcdoc` inside `about:blank`. They did not load the full original homepage or test browser HTTP `src` loading, deployed Pages, Safari, or the original runtime. The fixture marker is a layout sentinel, not a simulated working origin. A complete branch preview and Safari check remain before release. Source preservation is established separately by the GitHub diff.

No merge, deployment, ruleset change, or unrelated partner change is authorized by this record.

Reversal: remove only the marked `BEGIN ae-mow-first-frame` to `END ae-mow-first-frame` block from root index. Do not rewrite origin to roll back this mount.
