# doola referral iFrame · gated partner integration

Status: **disabled by default**. No production iFrame is embedded until a partner-specific approved URL is supplied.

## Confirmed
- Valentina Lugo's October 13 follow-up: referral iFrame is available; consultation booking iFrame expected the following week; Haliny Lone is the API/package contact.
- Public documentation: no-auth standard-account-creation iFrame is recommended for public pages. It describes a sandbox URL `https://app.development.aws.doola.com/embed/partner/[YOUR_UNIQUE_PARTNER_ID]` and requires doola to provide a unique partner snippet.
- SSO is a separate integration requiring a backend and shared secret; this static page does **not** attempt it.
- Existing affiliate handoff: `https://partnersps.doola.com/hhsoqhb23250`. Its attribution is **not** equivalent to proving iFrame attribution.

## To activate after partner verification
Edit the JSON block with id `doola-embed-config` in `doola/index.html`:

```json
{"enabled":false,"environment":"production","url":"","approval":"Await partner-specific doola-provided iframe URL and explicit launch approval"}
```

Only after receiving the exact partner-specific snippet from doola, verifying it with their team, and agreeing on attribution, use its authorized HTTPS URL and set `enabled` to `true`. Supported URL shapes are `https://app.doola.com/embed/partner/PARTNER_ID` and `https://app.doola.com/embed?partner_id=PARTNER_ID`, with sandbox analogs on `app.development.aws.doola.com`. **These URL shapes are provisional allowlisting, not proof that doola has supplied or approved such an exact production URL**. Never substitute a placeholder ID.

## Behavior
- No iframe element, network request to embedded doola, account provisioning, or user-data transfer is initiated before a visitor clicks the enabled button.
- If configuration is missing, disabled, or fails URL checks, the embed stays disabled and the original partner affiliate link remains usable.
- On activation the modal renders a third-party iframe with a clear provider label and separate “Open doola” fallback; closing removes the frame.
- User-entered founder information stays within doola's origin. No local intake answers are transmitted into the frame. No `postMessage`, token minting, checkout scripting, or cross-origin content reading.
- The existing public page remains an independent local business-preparation experience.

## Review checklist
- [ ] Partner-specific production **and sandbox** embed URLs provided by doola
- [ ] Confirm allowed parent origins, especially `https://xn--6ca.store` and any approved `github.io` URL
- [ ] Confirm referral attribution to this partner ID; compare with separate PartnerStack link
- [ ] Confirm doola terms, support, cancellation, security and privacy requirements
- [ ] Test on iPhone Safari and Android Chrome: iframe fit, internal scroll, virtual keyboard, frame blocked/cookie restrictions, fallback link
- [ ] Test desktop Safari/Chrome/Firefox: focus, Esc close, URL validation, frame failures and fallback link
- [ ] Confirm staging mode uses test accounts only
- [ ] Obtain explicit approval before promoting to production

## Sources
- doola Partner iFrame Public Docs (2025-11-05): https://doola.notion.site/Partner-iFrame-Public-Docs-292ff629db1e808a943ce8d3bf981237
- Valentina's follow-up (October 13): https://mail.google.com/mail/u/?authuser=yael.eureka%40gmail.com#all/1a137de46a207849
