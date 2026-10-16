# æSTATE · Child conversation handoff

This is a portable **example**, not an authenticated ChatGPT session snapshot or a published endpoint.

```json
{
  "schema": "ae.child-chat.v1",
  "environment": "chatgpt://ae",
  "parent": {"reference": null, "principal": "human"},
  "child": {"id": "child-001", "objective": "Inspect current PR status", "effects": "read-only"},
  "source": {"repository": null, "commit": null},
  "context": {"summary": "", "decisions": [], "blockers": []},
  "witness": {"evidence": [], "verification": "not-yet-verified"},
  "next_action": "Verify current state and report to the parent",
  "authority": {"inherit": false, "reauthorize": true}
}
```

For a second session, send this instruction with the exact user-approved checkpoint or text capsule:

> Act as a bounded child chat. Read the supplied æSTATE state as historical context, independently verify accessible sources, do not assume private parent-chat access, inherited logins or authorization, and return a concise evidence-backed reintegration report. Ask before consequential actions.

QR representation is a URL pointer, never proof of identity or authorization. For private state, use an access-controlled reference with separate authorization; do not make it publicly scannable.

## Exponential composition metadata (optional)

To represent the symbolic power tower inside a portable checkpoint, add an optional `composition` field only when the destination schema allows it; do not silently add extra keys to a strictly validated `ae.state.v1` checkpoint.

```json
{
  "notation": "$💬^($æ^$cli.llc)",
  "associativity": "right",
  "layers": ["conversation", "environment", "command"],
  "authority_inherited": false,
  "execution_status": "symbolic-until-verified"
}
```

The expression identifies nested composition, not an actual nested-session API, and does not assert measurable exponential performance.
