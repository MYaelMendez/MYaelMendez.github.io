# OpenSourceWare Boundary — væult

This file marks the **#opensourceware** release boundary for `væult/`.

> *We embody #opensourceware and equip new business owners with care.*
> Open Source Ware (evolution of OCW) — democratizes **agency**, not just knowledge.

## What væult is

A password-secured local vault: passphrase → scrypt → AES-256-GCM, with QR
air-gap transport. Custody stays on the operator's device; the QR carries the
**sealed** envelope, never plaintext. The whole thing is stdlib + `cryptography`.

## Included (shipped)

- `væult.py` — the vault: crypto, CLI, QR transport (single file, no package)
- `README.md` — usage + custody model
- `LICENSE` — MIT
- `release-manifest.json` — artifact hashes for this release

## Excluded (never shipped)

- **Any vault file** (`*.væult`) — an operator's encrypted secrets are theirs alone
- **Any passphrase**, in any form — never stored, never logged, never committed
- Operator-specific absolute paths (`C:\æ\secrets\...`) as *defaults* — the code
  ships with a neutral default and honours `VAEULT_PATH` / `VAULT_PATH` env overrides
- Private Hermes runtime assumptions — væult runs standalone on any Python 3.10+

## Generalization rules (what makes it OSW, not a personal script)

1. **No hardcoded operator identity.** The default vault path is a *convention*
   (`<root>/secrets/privateclient/privateclient.væult`), overridable by env.
2. **No network.** væult never makes a request. It cannot exfiltrate by design.
3. **No secret in argv, env output, or logs.** Values enter via hidden prompt or
   a caller-set env var; nothing prints a value except an explicit `get`/`export`.
4. **Degrade gracefully.** Missing `qrcode`/`pyzbar` disables only the QR commands;
   the core vault still works.

## Custody contract (the load-bearing rule)

```
secret  → stays on the operator's device, encrypted at rest
passphrase → never persisted; derived per-session
QR      → carries the SEALED blob; useless without the passphrase
network → never touched
```

If a downstream consumer needs a secret, it asks the vault to **perform the
action** and returns the result — the secret does not travel. See the GLOCAL
broker pattern (`CUDA_MCP²`): droplet brokers, Victus holds, only results cross.

## Boundary in one line

**The tool is open. The secrets are not.**
