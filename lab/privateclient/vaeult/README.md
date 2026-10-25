# væult

A password-secured local vault for sovereign secrets, with QR air-gap transport.

```
passphrase → scrypt(N=2¹⁵, r=8, p=1) → 32-byte key → AES-256-GCM (AEAD)
```

Single file, no package. Stdlib + `cryptography`. Never touches the network.

## Why

Your secrets should not live in a cloud you don't hold. væult keeps them
encrypted at rest on your own device, opens them per-session with a passphrase
you type, and can hand a **sealed** entry to another device by QR — where the QR
is inert without the passphrase.

## Install

```bash
pip install cryptography            # the only hard dependency
pip install qrcode pillow pyzbar    # only for the QR commands (optional)
```

## Use

```bash
python væult.py init                 # create the vault (passphrase ×2, min 8 chars)
python væult.py set STRIPE_KEY       # store (value read hidden)
python væult.py get STRIPE_KEY       # print to stdout
python væult.py list                 # entry names only — never values
python væult.py rm STRIPE_KEY        # delete (requires passphrase)
python væult.py export STRIPE_KEY    # shell-safe `export` line
python væult.py verify               # self-test: round-trip + tamper + name-binding
```

### QR air-gap

```bash
python væult.py qr STRIPE_KEY        # sealed entry → QR PNG
python væult.py qr-open qr.png       # decode + import (proves it opens under your key)
python væult.py qr-show STRIPE_KEY   # sealed payload as text
```

The QR carries `VAEULT1:{"blob":{...},"name":"..."}` — the **ciphertext**, not
the secret. Photograph it, print it, hand it across an air gap: it is useless
without the vault passphrase.

## Configuration

| Env var | Purpose | Default |
|---|---|---|
| `VAEULT_PATH` | vault file location | `C:\æ\secrets\privateclient\privateclient.væult` |
| `VAEULT_PASSPHRASE` | non-interactive unlock (scripts) | — (prompts via `getpass`) |

> Env var names are ASCII (`VAEULT_*`) on purpose — a rune in an identifier is
> not a valid POSIX shell variable, and `export VÆULT_…` fails.

## Design

| Property | How |
|---|---|
| Encrypted at rest | AES-256-GCM, fresh 96-bit nonce per entry |
| Tamper detection | GCM auth tag — a flipped byte fails closed |
| Name binding | entry name is AEAD associated data — a renamed entry won't open |
| Wrong passphrase | sealed sentinel → clear "wrong passphrase", not a crypto error |
| Atomic writes | write `.tmp` then `os.replace` |
| QR safety | carries the sealed envelope; no plaintext ever |

## Verification

```bash
python væult.py verify
# væult: verify OK
#   ✓ round-trip · ✓ tamper detected · ✓ name-binding enforced · ✓ AEAD AES-256-GCM
```

## Boundary

The tool is open. **The secrets are not.** See `OPENSOURCEWARE_BOUNDARY.md`.

## License

MIT — see `LICENSE`.

---

*#opensourceware · æ:// language is compute · #hermiphicationisinevitable*
