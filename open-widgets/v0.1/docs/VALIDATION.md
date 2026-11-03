# Validation / 2026-10-20

## Performed

- Node.js v22.16.0: syntax checks, relative-asset checks and browser-source boundary checks passed.
- `npm run check`: 33/33 automated tests passed, including real loopback HTTP requests to the local adapter/server with synthetic identities and a mocked OpenAI transport.
- Widget-model tests: four scenes, heterogeneous nesting, independent state, maximum depth/node budgets, fresh identities and private-state removal on fork/regrow, explicit null grants and private-state-free exports.
- Security/adapter tests: disabled/default denial, session expiry/scope, exact origin, fetch metadata, CSRF, explicit approval, strict schema, input/body/content-type limits, replay prevention, per-principal rate/concurrency and process budgets, redacted failures, request shaping, no tools, refusal/incomplete status, timeout/response limits, private static-file exclusion.
- Chromium offline DOM checks passed at 390x844, 320x700, 844x390 and 1440x1000. Checked full scene ratio, no document-level horizontal overflow, drawer/widget state through navigation, nested counter state through focus/Escape, fork/retire/regrow, reviewed JSON download excluding notes, text-not-HTML rendering, disabled adapter behavior and zero external requests.
- A browser-local mocked authorized session exercised one explicitly approved client request, safe output rendering and approval reset. No real credentials were used.
- Desktop and mobile screenshots were rendered and visually inspected.

## Testing limitation

Chromium URL navigation was blocked by the execution environment (`ERR_BLOCKED_BY_ADMINISTRATOR`), including loopback. Offline DOM tests therefore loaded local HTML/CSS in about:blank and flattened the two local ES modules. That verifies DOM interactions and responsive rendering, NOT real browser HTTP/ESM loading, secure cookies, CSP enforcement or provider connectivity. Node syntax and HTTP tests cover separate parts of the implementation.

## Not performed / not claimed

No live OpenAI API call, API-key access, model-entitlement check, authentication-provider implementation, remote browser, iPhone Safari/Android hardware test, full accessibility audit, production security assessment, GitHub Actions run, root-homepage change, OpenAI Site change, merge, deployment or partner operation.

Browser reproduction: `python tests/browser.py` in an environment with playwright and Chromium. DOM-only fallback: `AE_BROWSER_OFFLINE=1 python tests/browser.py`.
