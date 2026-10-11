# TEOTECH verification — October 11, 2026

Public-site checks performed approximately 09:22–09:33 America/Chicago. Baseline gh-pages commit: `02a41c4d4c86640c8f352a775663b06e6a3a0262`. Compared with merged PR #4 (`b29dfea8d223c2d9ec0dfe44475b4ca9eec37d7c`). Later commits have changed the theology hub since that merge.

## Verified public behavior

| Capability | Observation |
| --- | --- |
| Public deployment | Portal, learning journeys and theology hub return HTTP 200; portal and journeys render in Chrome. |
| Desktop layout | Portal hero, resource cards and journey form visually inspected at a 1363px viewport. Portal document width 1348px: no horizontal overflow at that width. This is a sampled inspection, not comprehensive visual approval. |
| Portal navigation | Portal-to-journeys and journeys-to-hub links work; portal resource anchor works through Enter. |
| Seven journeys | All seven lesson headings and scene links loaded in the public browser. Seven existing scene URLs return HTTP 200. |
| QR controls | All six portal controls open with Enter and close with Space; aria-expanded follows visibility. |
| QR destinations | Six portal SVGs and seven journey QR definitions rasterized on white and independently decoded with ZXing. All 13 exactly match their declared HTTPS destination, including journey fragments. Physical phone-camera scanning not performed. |
| Journal persistence | Explicitly saved Genesis notes and completion survived page reload. Blank required fields prevented completion. |
| JSON export | Actual browser download parsed successfully; schema `teologia.learning.v1`, timestamp and Genesis field contents were present. |
| Human boundaries | Test content was synthetic. No messages sent, memberships joined, classes accessed, certification granted, accounts changed, or PRs merged. |

The learning page contains seven QR definitions and displays the selected lesson's QR; it does not display seven lesson SVGs simultaneously.

## Reproducible defects and proposed changes

1. **Recorded completion reset by draft save.** Register all three fields, then click Guardar borrador: the public progress changes from 1/7 to 0/7. Preserve prior completion when saving edits; initial drafts remain incomplete and explicit registration still requires all fields.
2. **Unsaved edits lost on lesson navigation.** Type a note, switch lessons, return: the note is empty. Persist edits on input without rebuilding the form. Storage failures keep notes in memory with an export reminder. Completion is never created by autosaving an initial draft.
3. **Hub discovery links lost after PR #4.** The current public hub lacks TEOTECH and aprender.html links. Restore the original institutional card while preserving all six current canonical artifact cards. Repository history shows an earlier restoration (`ac2bd17`), followed by later changes; this is a recurring regression worth checking after future generated hub updates.
4. **Duplicate SVG path IDs.** The six portal QR paths all use `qr-path`. Remove these unused IDs without changing SVG geometry or QR destinations.

Saving and registering also restore keyboard focus to their respective buttons after the form redraw.

## External destinations

| Destination | Read-only retrieval result |
| --- | --- |
| æl.net root, /tech, /teologia-ai | HTTP 200 |
| YouTube @teologialatam | HTTP 200 |
| WhatsApp TECH invite | HTTP 200 |
| WhatsApp channel | Redirect to www.whatsapp.com, HTTP 200 |
| Classroom course | Redirect to Google sign-in, HTTP 200; course permissions and content unverified |
| Institutional LinkedIn | HTTP 999; destination content unverified |

HTTP availability does not establish resource ownership, current class announcements, invite validity after login, or suitability of all destination content. External services were not modified.

## Corrected-code validation

Run the focused regression suite with jsdom installed outside the repository:

```sh
npm install --prefix /tmp/teotech-qa --no-audit --no-fund jsdom
NODE_PATH=/tmp/teotech-qa/node_modules node tests/teotech-journal.cjs
```

Passed: required fields; input persistence across lesson changes; isolated notes; completion preservation; save-button focus; JSON contents; reload restoration; unavailable storage; six QR visibility/ARIA toggles; unique portal IDs; restored hub links; six current artifact cards preserved. `git diff --check` passed. These DOM tests validate the proposed correction; browser verification was performed on the published baseline, not the proposed branch.

## Remaining limits before publication

- **Mobile rendering remains unverified.** The available browser API did not expose viewport/device resizing. Keyboard shortcuts did not activate mobile emulation. Source includes portal breakpoints at 720/380px and journey breakpoints at 650/330px; their presence is not evidence of a successful mobile render. Review at 320, 390 and 768px, including expanded QR cards, long journal text and download behavior.
- Corrected branch needs desktop/mobile browser visual review before merging. A local file preview was blocked by the cloud browser's URL policy; no workaround attempted.
- Keyboard checks cover actionable controls and fields, not a full screen-reader or WCAG audit. Physical touch, iOS Safari, Android Chrome and printed output are unverified.
- Authenticated Classroom access and LinkedIn content remain unchecked. Biblical version/transcription attributions still need teaching-team review; no theological content changed.
- PR #4 contains a failed Cloudflare Workers deployment notice. GitHub Pages works; the Cloudflare failure was not diagnosed or changed.
- The seven separate æ.md PRs, banners, aeqr CI, local_agent task wording and Hark app permissions are outside this TEOTECH audit. No merge or permission change performed.

Publication decision: review and merge the corrective PR into gh-pages when ready. No production publication performed during this audit.
