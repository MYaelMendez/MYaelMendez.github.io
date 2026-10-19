---
name: sovereign
description: Use when an action needs authority — minting a capability, signing a kanban card, or gating a dispatch on a valid signature. The sovereign is the æ:// authority layer: Ed25519 custody that decides who may act, and until when. Wraps card_signing.py; never moves the secret — the key stays in C:\\æ\\secrets.
---

# sovereign · the authority layer

**Possession is not authority.** A kanban card carrying `{"cmd": "kanban://complete t_916"}`
is a route, not a grant. Anyone holding the bytes — a photograph, a printout, a
screenshot — can dispatch the same board mutation. The sovereign closes that gap: a
card becomes a **capability**, and only a holder of the signing key can mint a valid one.

Preserve **Many agents. One principal. Context may propagate; authority does not.**

## What it is

A thin, local authority layer over `C:/æ/agents/card_signing.py` (Ed25519, `cryptography`).
It binds a card to:

- the **exact command** — a signature cannot be replayed on another verb
- a **subject** — the operator or agent the grant is for
- an **expiry** — a photographed card stops working
- a **nonce** — optionally single-use, consumed on first verification

## The four verbs

| verb | does | returns |
|---|---|---|
| `sign` | mint a capability card | `{verb, task_id, subject, expires_at, nonce, sig, by, cmd}` |
| `verify` | gate a payload before dispatch | `{ok, reason, verb, ...}` — never raises |
| `audit` | list spent nonces + key fingerprint | `{fingerprint, spent_count, key_path}` |
| `keygen` | mint the signing keypair (once) | `{ok, private, public, fingerprint}` |

## The gate

Every dispatch passes through the same check, in order — each failure a distinct,
diagnosable reason:

1. the payload carries a signature → else `unsigned card`
2. the signature verifies against the public key → else `signature does not verify`
3. the card has not expired → else `card expired Ns ago`
4. (if single-use) the nonce is unspent → else `card already used (nonce spent)`

## Custody

The signing key lives at `C:\\æ\\secrets\\keys\\card.key` and **never** leaves custody.
The sovereign reads it by path; it is never printed, logged, or placed in a surface.
The conductor may *request* a signature; it may not *approve* one.

## Call it

    python C:/æ/agents/card_signing.py sign --verb complete --task t_916 --ttl 3600 --single-use
    python C:/æ/agents/card_signing.py verify '<payload json>' --consume

Surfaces may expose `æ.sign(verb, task_id)` / `æ.verify(card)` (code-mode) and the
`sign_capability` / `verify_capability` WebMCP tool contracts.
