# CHAT^chat|site|@GitHub.io

## Canonical interface

`CHAT^chat|site|@GitHub.io`

- `CHAT` = the human's conversational entry point.
- `^` = composition operator in our proposed notation.
- `|` = an explicit choice of a work surface, **not** simultaneous fan-out or authorization inheritance.
- `chat` = work inside the current ChatGPT conversation using available tools.
- `site` = open the **existing** OpenAI-hosted `openai_monosite` at https://yael-mendez.teologia-7508.chatgpt.site/ .
- `@GitHub.io` = open the versioned engineering and publication surface in the existing repository https://github.com/MYaelMendez/MYaelMendez.github.io . This does **not** mean that GitHub Pages is automatically deployed or synchronized.

Preserve the separate recursive composition `$💬^($æ^$cli.llc)` *inside* the chosen mode. Mode selection and exponential composition are separate concepts.

## Minimal state contract

```json
{
  "interface": "CHAT",
  "mode": "chat",
  "allowed_modes": ["chat", "site", "github.io"],
  "composition": "$💬^($æ^$cli.llc)",
  "mode_change": "explicit_user_choice",
  "shared_state": "nonsecret_versioned_reference_only",
  "session_transfer": false,
  "authority_inherited": false
}
```

## Operational checks

1. Chat: selecting chat does not navigate away. No invented ChatGPT URL or hidden session export.
2. Site: open only the already existing `openai_monosite`. Keep its identity and original content intact.
3. GitHub.io: distinguish repository links and published GitHub Pages links. Publishing requires a verified build and URL.
4. Switch: pass public checkpoint URLs only with explicit user intent; never transfer private conversations, credentials, tokens, or tool grants.
5. Witness: preserve source SHA, state of implementation, and the exact performed checks.

This file defines a proposed cross-surface interface. It does not implement native ChatGPT mode switching or an authenticated shared session.
