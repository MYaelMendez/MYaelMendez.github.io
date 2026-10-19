# RFC-æQR-0001 — Recursive Addressability of Agentic Environments

**Status:** Locked design doctrine · v1.0 (specification, not deployed protocol)  
**Project:** #OpenSourceWare (#OSW) → #InternetOfAgents (#IoA)  
**Principal:** HUMAN://principal

> **æQR makes the nested environment discoverable and portable.**  
> It gives intelligent work an address — a way to recover its context, a path to reuse, and a route to publication. Every widget carries its own æQR. Every loft can become a tower. Every tower can become a city.

## Doctrine

1. **Every widget has an æQR.** It identifies a stable, version-resolvable capability or work product, not a credential.
2. **Every loft can become a tower.** A contained environment may be independently addressed, forked, configured and published.
3. **Every tower can become a city.** A portable environment may become a discoverable index of subordinate environments and capabilities.
4. **Recursion preserves lineage, not authority.** Parent and child may share nonsecret context and provenance; no child inherits the parent's permission, identity or tokens.
5. **The human remains principal.** Every consequential effect requires its own valid authorization at the execution boundary.
6. **Witness closes the loop.** Results and lineage are recorded as evidence, with claims distinguished from independently verified execution.

## Address resolution contract (proposed)

An æQR encodes a **durable HTTPS resolver URL**. The resolver returns or points to a versioned manifest with:

- `id`, `version`, `kind` (`widget | loft | tower | city`)
- `canonical_url`, `parent_id` (optional), `children` (optional)
- `manifest_url`, `capabilities`, `required_permissions`
- `context_pointer` (nonsecret, access controlled as necessary)
- `issuer`, `provenance`, `witness_pointer`
- `fork_source`, `publication_status`

A QR payload MUST NOT contain access tokens, private user context, credentials, or implied authorization. Resolution is discovery; execution is a separate human-governed operation.

## Composition

```text
🫵 HUMAN://principal
    ↓ intent
🧩 WIDGET + æQR
    ↓ composition / fork
🚪 LOFT + æQR
    ↓ promote / publish
🏢 TOWER + æQR
    ↓ federate / index
🌐 CITY + æQR
    ↓ discover / interoperate
🛸 #InternetOfAgents
    ↓ verify
🧾 WITNESS → 🫵
```

**Invariant:** Context may propagate; authority does not.

**Thesis:** #OSW yields #IoA **when** open, portable work is made addressable, interoperable, permissioned, and verifiable. Open licensing or a QR code alone is insufficient.

## Implementation gates

- [ ] Implement and host HTTPS resolver.
- [ ] Define and validate the manifest JSON Schema and versioning rules.
- [ ] Generate an actual scannable QR from the resolver URL and decode-test it.
- [ ] Implement parent-child traversal, cycle prevention and fork lineage.
- [ ] Separate discovery from identity verification and per-effect authorization.
- [ ] Verify capability invocation and Witness receipts with real connected providers.
- [ ] Test portability across clients and publish the specification.

The existing `aeqr://widget/mcp/codex-micro` is **symbolic**, not a registered resolver or usable QR payload. This document fixes the design contract without claiming those implementation gates have passed.


## Amendment A — æ1 power tower integration (v1.1 design)

This amendment preserves the locked æQR doctrine and adds the human-centered æ1 environment model **before** resolver implementation. The expression `æ1 ^ æ2 ^ æ3 ^ æQR` denotes **nested, right-associative symbolic composition**, not numeric exponentiation, security guarantees, or independent autonomous principals.

### Layer responsibilities

| Layer | Alias | Responsibility | Not granted |
|---|---|---|---|
| æ1 | human agentic environment | Human intent, digital twin, twelve-floor life navigation, state and capability references | Universal access to accounts/devices |
| æ2 | `private_client` | Consent, privacy partitioning, disclosure controls, context minimization | Transfer of identity or permissions |
| æ3 | `soværeign_client` | Ownership, keys, governance, portability and revocation references | Authority by virtue of being nested |
| æQR | address layer | Durable address, manifest, provenance, fork and publication lineage | Authorization through scanning |

These are **conceptual roles and aliases**; no provider identity service, credential wallet or cryptographic key infrastructure is claimed as deployed. Historical æ¹/æ²/æ³ notations have also described API/DAO/CLI and MCP routing stages. This RFC uses the explicitly defined **æ1/æ2/æ3 human/privacy/sovereignty mapping** for its environment profile; other notations must be versioned or namespaced rather than silently conflated.

### æ1 human environment: twelve-floor navigation

`01 🏠 HOME` · `02 ❤️ HEALTH` · `03 📚 LEARN` · `04 ✝️ FAITH` · `05 🛠️ BUILD` · `06 🏢 BUSINESS` · `07 📈 ECONOMY` · `08 🌎 IMPACT` · `09 🏎️ MOVE` · `10 🏗️ CONSTRUCT` · `11 🧾 WITNESS` · `12 ⚖️ GOVERN`.

These are **user-customizable navigation categories**, not automatically authorized data sources. A floor may contain lofts; a loft may independently become a tower; a tower may publish a city. Promotion changes scope and addressability, not principal or permissions.

### æ1 environment manifest extension (proposed)

```json
{
  "schema": "osw.ae1.environment.v1",
  "id": "ae1.micro.demo",
  "kind": "widget",
  "version": "0.1.0",
  "principal": {"type": "human", "reference": "HUMAN://principal"},
  "layers": {
    "ae1": {"role": "human_environment", "twin": "unbound"},
    "ae2": {"alias": "private_client", "consent": "required"},
    "ae3": {"alias": "soværeign_client", "ownership": "human", "keys": "unbound"},
    "aeqr": {"status": "symbolic", "resolver": null}
  },
  "navigation": {"floor": "06", "floors": 12},
  "parent_id": null,
  "children": [],
  "capabilities": [],
  "permissions": {"inherit": false, "default": "deny"},
  "context": {"public_pointer": null, "private_payload": null},
  "witness": {"receipts": [], "verified": false},
  "publication": {"status": "draft", "fork_source": null}
}
```

This is a **nonsecret, proposed metadata contract**. A live implementation MUST store private context and grants outside the public manifest. Human authority is checked at invocation, not inherited from manifest text.

### Digital twin routing

```text
HUMAN://principal
   → æ1 intent + selected floor / loft
   → æ2 consent and context disclosure gate
   → æ3 ownership / authorization policy gate
   → æQR capability discovery (no implicit grant)
   → MCP or other VERIFIED adapter (if connected)
   → action-specific human authorization
   → execution → Witness receipt → human review
```

Device and model adapters are replaceable; neither a phone, keyboard, nor a specific model is the principal. `$mcp` and `$æ` are conversational aliases, not registered global commands. Real MCP integration requires a verified server, transport, tool contract and grants.

### Promotion and fork invariants

1. Every environment has a stable identifier and a version; every published environment resolves through HTTPS.
2. Widget → loft → tower → city is **promotion or federation**, not unbounded self-replication. Detect parent cycles and cap traversal.
3. Forks receive new IDs and explicit provenance; never copy secrets, credentials, tokens, private context or grants.
4. A QR code identifies a resolver URL; it is not a login, signature, approval or executable instruction.
5. The digital twin proposes and routes; **the human principal owns consequential decisions**.
6. Witness must distinguish proposed, simulated, dispatched, completed and independently verified states.
7. Context may propagate; authority does not.

### Revised first vertical slice

Build a single **æ1 widget** that exposes a selectable life floor, a portable public manifest, an æQR HTTPS URL and a parent/child preview. Test read-only discovery and fork export first. Add identity, consent, verified device/MCP adapters and execution receipts only through separate authorization gates. Do not publish user-private profiles or assert cross-client portability without tests.

**Acceptance:** Scan → Resolve → Inspect æ1 → Select floor → Fork without grants → Publish a new address → Verify lineage and Witness.
