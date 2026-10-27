# ChatGPT sign-in entry

The root and /work/ pages offer an optional, top-level link to the existing OpenAI-hosted Studio's platform-managed sign-in flow. They do not implement OAuth or receive a cross-origin session.

The link sends no local brief, profile, credentials, or execution grant. Connected-app consent and API spending authorization remain separate. Work in the local page can continue without signing in.

Verification on 2026-10-27: browser account selection returned to the Studio AI workspace with an authenticated identity. Connected-app access was declined during this identity-only test; generation remained disabled because API entitlement is separate. A bare request to /callback without an active authentication transaction is not a valid end-to-end login test.

No cross-site profile synchronization or repository authorization is implemented by these links.
