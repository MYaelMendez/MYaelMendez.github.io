# æLOCOMOTION

`æLOCOMOTION` (`ae-locomotion`) is the packaged name for the policy-driven
Asimov-1 gait harness. The `æ` marks it as an authority-bearing capability, not
a loose script: execution is gated by `HUMAN://ROOT` and every run is receipted.

The package lives at `packages/ae-locomotion/1.0.0/` and contains:

- a versioned `manifest.json` with authority, runtime, entrypoints, hashes, and the verified run;
- the ONNX checkpoint, `env.yaml`, `agent.yaml`, and source notice (BSD-3-Clause);
- the pinned MJCF base, visual, and physics-only variants with 23 policy actuators;
- the policy loop, renderer, publish pipeline, and the governance doc;
- `install.sh`, `verify.sh`, and `checksums.sha256`.

```bash
./verify.sh
HERMES_AE_POLICY_DIR="$HOME/.hermes/asimov-policy" ./install.sh
```

The name is deliberately short: **æLOCOMOTION** is what the harness is;
`ae-locomotion` is how it is addressed; `LOCOMOTION://` is how it receipts.

Published tarball SHA-256: `3bf52da6e02ecc51ad16ca6fb07bb8f1741a35fce1839a090fc5e5fe33288421`.
