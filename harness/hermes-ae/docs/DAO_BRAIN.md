# DAO Brain — Native Head Viewport

The DAO Brain powers the native Asimov head viewport as a **governance layer**, not an authority root.

```text
VISION / HUMAN / AGENT PROPOSAL
→ æ Policy evaluation
→ DAO Brain decision + viewport state
→ tiny-voca reply (optional)
→ DAO://DECISION receipt
```

## Canonical binding

- Engine: `scripts/daobrain.py`
- Policy source: `ae-policy.json`
- Face state: `$HERMES_HOME/ae/asimov-face.json`
- Op: `ae({op:"daobrain", action:"status"|"propose"|"state"|"verify"})`
- Receipt actions: `DAO://DECISION`, `DAO://STATE`
- Authority: `HUMAN://ROOT`

## Face states

| State | When |
|---|---|
| `IDLE` | no active proposal |
| `LISTENING` | allowed read-only observation |
| `THINKING` | deliberation in progress |
| `SPEAKING` | tiny-voca reply is active |
| `AWAITING_APPROVAL` | policy returned `require_approval` |
| `APPROVED` | human approval or armed deadman exists |
| `REFUSED` | policy denied the proposal |
| `ERROR` | engine failure or unknown decision |

## Propose a decision

```json
ae({
  "op": "daobrain",
  "action": "propose",
  "actor": "vision-model",
  "source": "vision-model",
  "intent": "publish",
  "speak": true,
  "voice": "M2"
})
```

The DAO Brain evaluates the proposal through `ae_policy.py`, writes the decision into the head viewport's `dao_brain` state, optionally speaks the reply with tiny-voca, and appends a `DAO://DECISION` receipt.

Example outcomes:

| Proposal | Decision | Face state |
|---|---|---|
| vision model asks to publish | `require_approval` | `AWAITING_APPROVAL` |
| same proposal with human approval | `allow` | `APPROVED` |
| Pi500 teleop with `arm + deadman` | `allow` | `APPROVED` |
| QR used as permission | `deny` | `REFUSED` |
| read-only observation | `allow` | `LISTENING` |

## Authority boundary

The DAO Brain can deliberate, route, and render state. It cannot sign for the human.

```text
DAO decides ≠ DAO authorizes
policy allow ≠ human approval
face state ≠ receipt
```

All approvals must still be bound by `HUMAN://ROOT`, an action hash, and an expiry. Motion additionally requires an armed deadman.

## Integration

`ae({op:"head","action":"status"})` now reports the live `dao_brain` block alongside face mode, voices, keymap, and ledger head. The head viewport therefore shows not just a viseme surface, but the current governance decision behind it.
