# Secure backend adapter contract / v0.1

Status: implemented reference adapter; disabled by default. Unit and local HTTP tests use synthetic identities and mocked provider responses. No production keys, live account access, or hosted authentication service have been configured.

## Boundary

Browser -> same-origin authenticated host -> server-only adapter -> OpenAI Responses API.

The browser never supplies an API key, model, upstream URL, tool definitions, system instructions, identity, repository, or agent grant. It sends only an explicitly approved text intention. No automatic retries; no tool execution. An error or timeout may still incur a provider charge if the provider received the request.

The host must serve the UI and adapter behind the same origin. Static GitHub Pages can serve the four UI files, but cannot run the Node adapter. An authenticated backend/reverse-proxy integration is a separate deployment decision. No deployment is included here.

## Trusted host authentication

`createAdapter({origin, enabled, authenticate, provider})` defaults to `enabled:false`, a null provider and an authenticator that returns null.

A reviewed SERVER-SIDE `authenticate(req)` must independently validate a real session, not trust browser-supplied identity headers. It returns:

```js
{
  id: "opaque-server-principal",
  expiresAt: 1792530000000, // example only; must be a future epoch millisecond time
  scopes: ["ae:respond"],
  csrfToken: "random-session-bound-base64url-at-least-32-characters"
}
```

Otherwise it returns null. The included launcher loads this function only from an operator-configured absolute `AE_AUTH_MODULE` path. There is no permissive production or development auth bypass.

A production host needs secure HttpOnly, SameSite cookies over HTTPS; server-generated CSRF tokens; revocation/expiry; login abuse controls; verified account entitlements and explicit user quotas. None of those are created by a static widget, a plugin symbol, a parent widget or an imported manifest. Request approval is separate from account authentication.

## GET /api/ae/session

Requires enabled adapter, exact Host, compatible fetch-origin metadata, trusted nonexpired session and `ae:respond` scope. No model invocation.

Success: `{ready:true, csrf_token:string, expires_at:number, capability:"text_only", provider_access:"not_tested_by_session_check"}`.

The frontend keeps the CSRF token in memory only. A successful session check is not proof that OpenAI credentials or model access work.

## POST /api/ae/respond

Requires exact Origin/Host; allowed fetch-site metadata; a verified session/scope; `X-AE-CSRF`; JSON content type; and all fields below. No unknown fields accepted.

```json
{
  "request_id": "11111111-1111-4111-8111-111111111111",
  "prompt": "Help plan a classroom widget environment.",
  "approved": true
}
```

`request_id`: UUID v4. `prompt`: nonempty text, maximum 2,000 characters. `approved`: true for this exact request, not a blanket execution grant. Request body limit: 8 KiB; compressed requests are rejected. Browser approval resets whenever the prompt changes and after each attempt.

Success: `{text, status, receipt}`. Status remains `completed`, `incomplete` or `refused`. Text is rendered using textContent, never interpreted as HTML or executed. Receipt includes request correlation, observation time, provider/model identifiers and reported token usage; it contains no prompt or private widget state. Receipts are not cryptographic attestations.

Errors use a short redacted code and correlation UUID, never upstream bodies, keys, prompts or stack traces. Relevant statuses: 400 invalid schema, 401 identity, 403 origin/scope/CSRF/approval, 409 duplicate attempt, 413 size, 415 content type, 429 limit, 503 disabled, 502/504 upstream failure. CORS is not enabled.

## OpenAI transport

Fixed endpoint: `POST https://api.openai.com/v1/responses`.

Server configuration chooses the model and sets the API key via `OPENAI_API_KEY`. Explicit user-role input, fixed application instructions, `tools:[]`, `tool_choice:"none"`, `store:false`, `stream:false`, default `max_output_tokens:768` (configurable only server-side, bounded 16-2048), 25-second timeout, no redirects and 1 MiB response limit.

Only assistant text/refusal items are extracted. Tool-only or failed output is not reported as successful text generation. The local server emits no prompt/key logs. `store:false` is not a zero-retention guarantee: OpenAI's abuse-monitoring and other applicable data controls still apply.

## Pilot usage guardrails

Per process: 6 admitted requests per minute per principal, 1 in-flight request per principal, 2 in-flight requests globally, and 50 total admitted attempts for the process lifetime. Failures consume the attempt budget too. Duplicate IDs are blocked for 5 minutes, including failed attempts. Replay/rate maps are bounded.

These are single-process request limits, not exact token/dollar budgets or durable global idempotency. Restarting the process resets them. Before production, use shared atomic quota accounting, persistent idempotency/audit policy, global request limits, account-level spend controls, verified pricing/model limits and operational monitoring. Never expose a free-for-all public proxy billed to the owner.

## Official references checked 2026-10-20

- Responses create: https://developers.openai.com/api/reference/resources/responses/methods/create
- Text generation: https://developers.openai.com/api/docs/guides/text
- API-key safety: https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety
- Data controls: https://developers.openai.com/api/docs/guides/your-data

These support the provider request and credential-handling choices. They do not certify this custom adapter or grant access to the user's account.
