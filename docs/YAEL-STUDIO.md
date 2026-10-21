# YÆL × æ Studio · Integration Contract

## One system, two layers

**YÆL** is the human/principal interface.

**æ Studio · Agentic Environments** is the environment, composition, and runtime layer.

They are not duplicate products and should not compete for the same role.

## Default posture

**Return value to the human. ❤️ Work here.**

The current ChatGPT conversation is the default working surface when the task can be completed there. Site handoff is optional and explicit.

- Studio App: `app://asdk_app_sites_047a09edddd88191806fef7a539628a8`
- YÆL Plugin: `app://plugin_b608fd3fbe548191964ac63c347f2f0f`
- Existing public Site: `https://yael-mendez.teologia-7508.chatgpt.site/`

## Native GitHub

GitHub is a first-class Studio capability, not a handoff.

The Studio should be able to inspect and work with repositories, branches, commits, diffs, pull requests, issues, reviews, workflow runs, and CI status directly through the connected GitHub capability.

```text
YÆL
  → Work here
  → æ Studio
      ↔ GitHub://repositories
      ↔ GitHub://branches
      ↔ GitHub://commits
      ↔ GitHub://pull-requests
      ↔ GitHub://issues
      ↔ GitHub://actions
  → review
  → HUMAN://principal
```

GitHub is the versioned engineering memory and review surface. It does not become the principal and repository permissions do not expand human authorization. Creating source changes, opening a PR, merging, deploying, and publishing remain separate actions.

## Shared loop

```text
HUMAN://principal
  → intent
  → Work here
  → æ Studio capabilities
  → GitHub-native source / review when appropriate
  → review
  → authorized execution
  → witness
  → HUMAN://value ❤️
```

## Invariants

1. The human remains principal.
2. Context may propagate; authority does not.
3. Navigation, QR, plugin invocation, copying context, model selection, or opening the Site do not transfer authority.
4. Private intention, credentials, grants, and private conversation state do not enter public artifacts by default.
5. Proposal, source change, test, execution, deployment, and publication are separate states.
6. Chat and the existing OpenAI Site remain peer destinations; no automatic synchronized private session is assumed.

## Product language

**YÆL × æ Studio**  
**Human-Owned Agentic Environments**

**Many agents. One principal.**  
**Return value to the human. ❤️ Work here.**
