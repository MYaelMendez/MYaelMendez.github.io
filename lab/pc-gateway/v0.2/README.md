# PC:// gateway v0.2: la capa del principal (lab · DEMO)

Built from first principles: one file, zero dependencies, Node ≥ 18. **Many agents. One principal.**
doola (formation) runs underneath as `capability://formation`. PC:// never rebuilds the legal rail; it holds identity, authority and receipts.

## Patterns
| Pattern | In PC:// |
|---|---|
| Two keys, two powers | `pc_sk_` = principal (droplet only) · `pc_ss_` = short, scoped, revocable agent session |
| Sessions minted by the principal | `POST /v1/sessions` · `*` and human_only capabilities can never be delegated |
| Idempotency = receipt | every POST needs an `Idempotency-Key`; replay returns the same answer, reuse with a different body → 409 |
| Required actions = human gate | agent writes become `PENDING`; only the principal approves or denies; the action id is the upstream Idempotency-Key |
| Events, not polling | signed doola webhooks (`X-Doola-Signature`, HMAC-SHA256) + `POST /v1/reconcile` |
| Fixed envelope | `{payload, error}`; branch on `error.code` |
| Evidence | append-only SHA-256 chain from GENESIS, `GET /v1/receipts/verify` |
| Docs for agents | `GET /llms.txt` · public `GET /v1/manifest` (pc.manifest/0.2) |

## Run
```bash
export PC_PRINCIPAL_KEY=pc_sk_$(openssl rand -hex 24)
export PC_SESSION_SECRET=$(openssl rand -hex 32)
export DOOLA_API_KEY=dk_test_…          # sandbox key; never commit it
export DOOLA_WEBHOOK_SECRET=wk_…        # from the doola Partner Portal
node server.mjs                          # listens on 127.0.0.1:8787
node test.mjs                            # end-to-end against the doola sandbox
```
On the droplet: keep the env in `/etc/privateclient/pc-gateway.env` (chmod 600), run it under systemd, and put Caddy in front with TLS (webhooks need HTTPS). Take a snapshot and set the firewall first. Live keys (`api.doola.com`) only after the agreement is signed.

## Test (2026-10-21, doola sandbox): 19 passed · 0 failed
manifest public · unauthenticated rejected · session minted without `*`/`pay` · idempotent replay · 409 on key reuse · 400 without key · agent can't mint · agent reads WY LLC fee ($100) · agent write → required action · agent can't resolve · principal approves → doola creates customer · no double resolve · signed webhook ok · forged webhook rejected · reconcile · revoked session dead · chain verifies.

Read-only DEMO in the lab. No secrets in the repo. Evidence ≠ Authority: the gateway informs; the human decides.
