# æ Policy

`æ` is the OpenSourceWare authority policy that robots and agents can leverage in the Internet of Agents. It is machine-readable, enforceable, fail-closed, and receipted.

```text
HUMAN://ROOT → æ → ae → harness → RECEIPT
```

## Canonical artifact

- Policy: `ae-policy.json`
- Engine: `scripts/ae_policy.py`
- Op: `ae({op:"policy", action:"show"|"verify"|"evaluate"})`
- Receipt action: `POLICY://EVALUATE`
- Authority: `HUMAN://ROOT`

## Core rules

| ID | Rule | Enforcement |
|---|---|---|
| `AUTH-001` | `HUMAN://ROOT` is the only authority root | deny |
| `AUTH-002` | Agents may propose; they may not authorize | require approval |
| `AUTH-003` | A QR is an address, not permission | deny |
| `AUTH-004` | Read-only observation is allowed with actor identity + receipt | allow |
| `ACT-001` | Actuation requires human approval or an armed deadman | require approval/deadman |
| `ACT-002` | Commerce and payment are drafts until the human signs | require approval |
| `PUB-001` | External publication requires approval + public receipt | require approval |
| `EVID-001` | Every decision writes a receipt | receipt required |
| `FAIL-001` | Unknown actions, missing actors, expired approvals fail closed | deny |

## Evaluate a request

```json
ae({
  "op": "policy",
  "action": "evaluate",
  "request": {
    "actor": "external-agent",
    "action": "publish",
    "source": "agent_message"
  }
})
```

Response: `decision: "require_approval"`, `allow: false`, rules `AUTH-002` + `ACT-001`, and a `POLICY://EVALUATE` receipt.

To approve:

```json
"approval": {
  "human": true,
  "action_sha256": "<sha256 of exact request>",
  "expires_at": "2030-01-01T00:00:00Z"
}
```

Pi500 teleop may use an armed physical deadman instead:

```json
"controls": {"arm": true, "deadman": true}
```

## Machine bindings

| Machine | Role | Obligation |
|---|---|---|
| `hermes-ae` | runtime / MoH router | enforce before dispatch; receipt every decision |
| `asimov-agent` | embodied executor | act only through a governed harness |
| `asimov-viewport` | public projection | read-only; never mutate authority |
| `commandprompt-ai` | 1:1 command glass | render prompts and receipts; never sign |
| `privateclient-ai` | approval gate | drafts become signed actions only by human approval |
| `pi500-teleop` | keyboard fallback | arm + deadman; receipt every command |
| `android-mcp` | phone transport | context and gestures only; never root |
| `llm-store` | commerce surface | carts/checkout are drafts until human signs |

## Failure behavior

`fail_closed: true`. Missing actor, unknown action, invalid authority claim, revoked actor, QR-as-permission, or expired approval always denies. A `require_approval` decision is never an allow.

## Verification

```json
ae({"op":"policy","action":"verify"})
```

Checks policy hash, authority, glyph, chain, rule count, bindings, and unified ledger integrity.
