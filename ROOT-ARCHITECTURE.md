# æææ.com Root Architecture

**Status:** canonical public architecture  
**Root:** https://æææ.com  
**Source fabric:** https://MYaelMendez.github.io  
**Lineage:** Git

## Separation of concerns

```text
HUMAN://ROOT 🧿
      │
     >_
      │
   æææ.com
CANONICAL ROOT
      │
 discover · resolve · ontology · policy · provenance
      │
     ➿➿➿
      │
MYaelMendez.github.io
PUBLIC SOURCE FABRIC
      │
 specs · runtimes · labs · demos · research
      │
    >_://|||
 ┌────┼────┐
 ▼    ▼    ▼
🛸₁   🛸₂   🛸₃
a₁    a₂    a₃
🧵₁   🧵₂   🧵₃
 └────┼────┘
      🪡
      🧶
      ↺
```

## Constitutional rule

> Context may propagate; authority never propagates implicitly.

- **æææ.com is thin:** stable namespace, index, resolver, ontology, policy and provenance pointers.
- **GitHub.io is deep:** public specifications, applications, WebGPU/WebMCP/WebLLM experiments, reference implementations, research and demos.
- **Git is lineage:** commits, diffs, branches, tags and releases provide inspectable provenance.
- **🛸 is an isolated agentic sandbox:** a bounded computational vessel containing an actor, permitted context, tools, compute, policy and delegated authority.

## Resolution contract

An æææ root route SHOULD identify a canonical object and resolve to its public artifact without pretending the artifact lives at the root.

```text
https://æææ.com/primitive
        ↓
æææ://primitive
        ↓
https://MYaelMendez.github.io/PRIMITIVE.md
```

The transport remains HTTPS. `æææ://` is the agentic namespace abstraction.

## Root namespace

```text
æææ://
├── primitive
├── protocol
├── spec
├── discover
├── agents
├── capabilities
├── compute
├── memory
├── receipts
└── labs
```

## Execution grammar

```text
>_    INVOKE
://   RESOLVE
|||   PARALLELIZE / PROVISION ISOLATED EXECUTION
🛸    ISOLATED AGENTIC SANDBOX
aᵢ    COMPUTATIONAL ACTOR
🧵    EXECUTION / EXPERIENCE
🪡    COMPOSE
🧶    RETAINED STATE
🧿⌚️  LIVING MEMORY
↺     REINTEGRATE
```

**Compute may distribute. Cognition may multiply. Authority remains human. 🧿**
