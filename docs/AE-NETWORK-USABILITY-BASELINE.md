# æ · Network Usability Baseline
Status: DESIGN REFERENCE · 2026-10-14

Canonical engineering and economic specification:
https://github.com/MYaelMendez/llm.store/blob/main/spec/RFC-0002-NETWORK-QR-ECONOMY.md

## Consolidated experience
One mobile-first 9:16 viewport; transparent interchangeable widgets; colored moving signal rails; emoji + text entry; discover/engineer/govern lanes; accessible motion controls.

## Entry points
`$æ` / `$ae` (ASCII fallback), `$🏡` household, `🤝` permissioned connection, QR versioned web link, `#startabusiness` pathway.

## First test
`▦ → 🏡 → 🤝 → verified service value → settled revenue → measured cost → ♻️ reinvest`.

Show real transaction receipts and transparent economics, not animated mock earnings. Publish no household or medical personal data in analytics.

## Network principle
One source of truth, many branded views. Domains and repos reference the same versioned contract; they do not automatically sync, execute, or acquire permissions.

## Status
Documented design, not a claim of deployed functionality.

## Universal widget chrome: OpenAI model picker + QR badge (2026-10-14)
Every independently mounted widget SHALL display:
- `🧠ᵐ` OpenAI model/profile picker in its header. Default `Auto`; present only models actually available and suitable for that widget. Do not hardcode or imply entitlement.
- `▦ᑫ` QR badge adjacent to the picker. QR resolves to a versioned, publicly shareable HTTPS widget descriptor/entrypoint; never embed secrets or private session state.
- Accessible labels, keyboard navigation, mobile tap targets, and reduced-motion behavior.
- An explicit distinction between **design preview** and **connected execution**.

Suggested descriptor:
```json
{
  "schema": "ae.widget.v1",
  "widget_id": "home",
  "widget_version": "1.0.0",
  "entry_url": "https://example.org/ae/widgets/home",
  "model_profile": "auto",
  "allowed_capabilities": [],
  "principal_authority": "not-transferred",
  "receipt_policy": "on-consequential-action"
}
```
The URL is illustrative. Model selection is local to the widget and must be validated server-side. A QR scan never grants authorization. Do not display fabricated live status or model routing.
