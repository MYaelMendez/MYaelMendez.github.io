# menlo-asimov-ffmpeg v20261117-d8c65a2

Official Menlo Research Asimov-1 source visualized straight through the
OpenSourceWare ffmpeg harness. No institutional endorsement claimed.

```text
HUMAN://ROOT → Menlo MJCF/URDF → PIL frames → ffmpeg → OSW gallery → receipt
```

## Deploy

```bash
export PAGES_DIR=/path/to/MYaelMendez.github.io
export ARTIFACT_DIR="$(pwd)/assets"
./deploy.sh
```

If `gh` is unavailable, deploy.sh uses plain git: `git add`, `git commit`,
`git push origin gh-pages`. The human holds the credentials.

## Verify

```bash
export BASE_URL=https://raw.githubusercontent.com/MYaelMendez/MYaelMendez.github.io/gh-pages/ffmpeg-asimov
./verify.sh
```

The zip is the #osw boundary: the agent holds the artifact, the human holds the gate.
