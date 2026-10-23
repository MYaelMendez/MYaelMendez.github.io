# CHAT^Codex|Dots|@GitHub · integration contract

Recorded: 2026-10-16. State: **proposed integration**, not a running connection.

## Roles

- **CHAT / $💬**: human-directed conversational cockpit; chat mode and site-like ChatGPT view can both express intent.
- **Codex**: code inspection, changes and tests in an authorized project environment. Codex Cloud requires an eligible account and a prepared/published cloud environment, with repository permissions independently verified.
- **Dots**: optional ongoing project stewardship, research, scheduling and progress reports, where an eligible account has a dot enabled. An eligible dot can create Codex Cloud tasks after the Codex environment exists, but this repository cannot start or bind a dot on its own.
- **@GitHub.io**: versioned source, reviews, GitHub Actions and—if published—static pages. A GitHub repo is not an authenticated ChatGPT session.
- **æSTATE + æQR³**: portable *nonsecret* handoff pointer and witness; secrets, permissions and private conversation history never transit in a public QR.

The composition is **right-associative**: `$💬^($æ^$cli.llc)`. Codex and Dots are **available capability adapters** within an authorized environment, not extra exponent terms that bypass approval.

## Honest capability matrix

| Surface | Today in repo | Requires |
| --- | --- | --- |
| Native in-chat site-like UI | Supported at conversation response level, not deployed by this repo | Host rendering and explicit user interaction |
| OpenAI-hosted æ Studio | Existing separate Site; source not editable via this GitHub repository | Site editor/source access and separate deployment verification |
| Codex Cloud | No authenticated cloud environment verified by this repo | Eligibility, setup on web/desktop, GitHub repo access, task run receipt |
| Dot | Not connected or started by this repo | Eligible rollout, initial dot setup on desktop web/app, chosen permissions |
| GitHub repository | PR #21 is versioned and reviewable | Merge, publish and runtime tests require separate authorization |
| æQR resume | Spec and generator are in separate PR #20 | Merge/public endpoint, QR scan/browser test, second-session verification |

## First vertical slice: inspect → build → review → steward

1. Human selects **Codex** and approves a narrow task: inspect `MYaelMendez/MYaelMendez.github.io` PR #21 for accessible Native SVG and responsive chat/site/source navigation.
2. With an eligible, connected environment, Codex checks out the precise source revision, runs tests, proposes changes on an isolated branch or task, and returns a diff and test receipts.
3. Human reviews changes. Merge/publication is a separate decision.
4. If Dots is available, configure a dot (via supported desktop setup) to review the same repo and Codex task results periodically and surface decisions, **without** autonomous merge/deploy.
5. Save the verified public source revision and evidence to æSTATE, then offer an æQR³ resume link after it is actually published and scanned.

## Human-facing setup

- Codex: open https://chatgpt.com/codex and create/publish an environment connected to the intended GitHub repository, where eligible.
- Dots: open https://chatgpt.com/dots on desktop web or desktop app to check availability and set one up. Dots rollout and eligibility may vary. If enabled, provide the Codex environment and scoped assignment.
- GitHub: review https://github.com/MYaelMendez/MYaelMendez.github.io/pull/21 .

## Guardrails

**Many agents. One principal. Context may propagate; authority does not.** Do not mark an integration ready merely because a provider exists. Preserve independent authentication and human review. Keep chat, Site, and GitHub as separate working surfaces with optional handoffs, not an invented shared session.

Official reference:
- https://help.openai.com/en/articles/20001530-getting-started-with-your-dot
- https://help.openai.com/en/articles/20001545-using-codex-cloud
