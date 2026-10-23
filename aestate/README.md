# æSTATE v1 · GitHub checkpoint handoff

**Status:** Review-only reference implementation. No automatic ChatGPT session restoration, deployment, or permission sharing.

- `schema.json`: declared public checkpoint fields.
- `checkpoints/emoji-pr19.json`: historical reference checkpoint, pinned to previously observed website PR head `f7cd5b0`.
- `validate.py`: zero-dependency structural validator; checks deny-by-default authority, versioned source SHA, public witness URL, and common secret markers. Not full JSON Schema validation.
- `index.html`: QR code generated in the browser. Requires external qrcodejs library; scan-test required.

The sample QR encodes the immutable source URL:
`https://raw.githubusercontent.com/MYaelMendez/MYaelMendez.github.io/9ca3b76be1d5bea52dd826b0e8552c74ff1f15bc/aestate/checkpoints/emoji-pr19.json`

This references the checkpoint committed in `9ca3b76`, not a mutable branch alias. Verify HTTPS accessibility and raw response before distributing.

## Resume in any ChatGPT session
1. Scan QR or copy the HTTPS URL; never encode a credential or private conversation in public QR.
2. Ask ChatGPT to fetch the JSON and inspect the pinned commit and referenced source.
3. Treat checkpoint status as **historical**. Reinspect actual PR and build state.
4. Inspect witness provenance and request fresh authorization for any write or deployment.

## Run
`python3 aestate/validate.py` (Python 3.10+, standard library).
The workflow `ae-state-validate.yml` checks pull-request changes with read-only token permissions. No automated publish step exists.

**Context may propagate; authority does not.**
