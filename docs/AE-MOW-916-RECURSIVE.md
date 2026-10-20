# æ Studio · 9:16 recursive carousels and Mixture of Widgets (MoW)

**Status:** Preserved architectural decision and proposed implementation contract, 2026-10-20. This document records design intent; it does not assert the functionality is deployed.

## Non-negotiable intent

**Full 9:16 is the native canvas, not a design constraint.** An æ carousel presents **whole 9:16 environments**, not compressed mini-cards. Every frame can be an independent interactive world with its own state, controls, drawers, and other complete widget environments. The UI may adapt to other viewports; 9:16 remains a first-class compositional unit.

**Widgets within widgets within widgets.** Nesting is recursive. Every widget may be a host for a drawer, carousel, widget, and heterogeneous mixture. The interface has no conceptual fixed nesting ceiling; implementations need measurable rendering, memory and accessibility budgets. Keep deeper worlds discoverable without cramming them into miniature unreadable cards: expand, focus, zoom, detach or navigate inward.

**Mixture of Widgets (MoW)** composes unlike capabilities (e.g., 💬 Chat, ⌨️ Code, 🤖 Agents, 📧 Mail, 🗺️ Map, 🎞️ Media, 📊 Data, 💳 Commerce), not just multiple copies of the same card. A mixture may itself be nested inside a widget, giving a **Mixture of Mixtures of Widgets (MoMoW)**. This is composability, not an assertion that every provider connection is active.

### Three structural primitives

- **Carousel = breadth:** navigate between complete 9:16 environments (each a full scene), independently addressable, swipable, keyboard-accessible.
- **Drawer = depth:** expand/collapse capabilities inside an environment without destroying their state. Drawers themselves may contain nested widgets or more carousels.
- **Mixture = composition:** orchestrate heterogeneous, independently typed widgets in the same environment. Each widget may contain a child mixture.

The pattern is **Widget → Drawer → Carousel → Environment → Loft → Tower → City → æææ**, but these are reusable compositional roles, not a mandatory one-way hierarchy. A carousel can live inside a widget; a widget can host another carousel; a drawer can host a whole environment. Allow composition in either direction and recursive nesting.

### Coordinates and recursion

- Origin: `x0:y0:z0:æ:æ`
- Public review: `x0:y0:z:0:æ:æ:æ`
- Canonical symbolic invocation: `>_æææ://|||`
- Root: `HUMAN://ROOT`
- `æ → æ(æ) → æ(æ(æ)) → …` is conceptual recursion, not an infinite runtime or a permission chain.
- Address layers are descriptive references only. **Context may propagate; authority does not.**

## Foundational dependency: models → agents → viewport code → widgets

**Creator's clarification, 2026-10-20:** "The mixture of widgets is only possible today after mixture of models, agents and viewport code."

For this architecture, **Mixture of Widgets is the interface-level synthesis of model composition, agent coordination and executable viewport composition**—not a collection of decorative dashboard cards. Preserve this lineage when implementing or describing MoW.

1. **Mixture of Models (MoM):** independently selected model capabilities, each with explicit inputs, outputs and provenance. Here this means composing model services, not asserting a particular model's internal mixture-of-experts architecture.
2. **Mixture of Agents (MoA):** task-oriented participants coordinate capabilities through defined responsibilities, bounded context, permissions and completion checks. This is our architectural usage, not a claim to implement a particular published multi-agent algorithm.
3. **Viewport code composition (working shorthand: MoV):** independently operable interfaces render controls, state and interactions across full 9:16 scenes, drawers and nested surfaces. A viewport contains executable interface code, not merely a picture. MoV is a local working label, not an established external standard.
4. **Mixture of Widgets (MoW):** these model- and agent-connected surfaces become heterogeneous, independently stateful, recursively composable units. Each can contain another mixture (MoMoW).

**Architectural lineage:** `MoM → MoA → viewport code → MoW → MoMoW`, with feedback between layers. This describes the proposed system's enabling layers, not a universal historical claim that ordinary widgets or nested interfaces were previously impossible. It does not require every widget to invoke an LLM, nor establish that any particular integration is connected.

A composed widget keeps **model bindings, agent responsibilities, viewport implementation, child composition, local state, provenance and authorization requirements** distinct. A visual container never grants a model, agent or child widget permission to act.

**Design consequence:** carousel navigation exposes complete environments; drawers open their internal capabilities; recursive mixtures make the underlying models and agents usable through those environments. The intelligence, operations and interface are composed together under one human principal.

## Container and widget contract (proposal)

```ts
type WidgetNode = {
  id: string;                    // stable, nonsecret ID
  kind: string;                  // chat | code | agents | mail | map | media | ...
  viewport: { preferred: "9:16"; responsive: true };
  presentation: "scene" | "carousel" | "drawer" | "tile" | "focus";
  children: WidgetNode[];        // recursive, bounded by renderer safeguards
  localState: unknown;           // per-widget, never implied shared credentials
  inputs: CapabilityReference[]; // explicit typed connections
  provenance: EvidenceReference[];
  principal: "human";
  grant: null;                   // grants never inherited from parents
  implementationStatus: "proposal" | "local" | "verified" | "connected";
};
```

Design notes:
1. A **carousel item** is a whole independently operable 9:16 scene, with its own inner drawers, not a thumbnail-only card. Permit multiple carousels inside an environment and carousel-within-carousel when usable.
2. A **drawer** preserves child widget identity and state while hidden. Opening/closing does not execute provider actions. Offer accessible labels, focus management, and keyboard controls.
3. A **mixture** has explicit typed interfaces between children; no arbitrary shared global state. Local composer interactions and real external execution must be visibly distinguished.
4. **Nested widgets** keep stable IDs, local state, capability declarations, provenance, and explicit authorization boundaries. No parent passes secrets or grants implicitly.
5. **Fork** produces a separate addressable configuration with lineage and no inherited permissions. QR shares a public reference to the selected widget or scene, not secrets or session state.
6. Responsive canvases preserve 9:16 scene semantics even when desktop displays several scenes at once. Include motion pause, reduced-motion support, readable full-screen focus, zoom, and assistive navigation.

## First interactive carousel collection

Each is a complete 9:16 environment with independently operable drawers:

| Frame | Full environment | Example drawers |
| --- | --- | --- |
| 01 | ☺ Origin / human intention | ❤️ Principal; ⌨️ CLI; 🧠 Context; 🪪 Identity |
| 02 | 🧩 Widget Factory | 🔍 Discover; 🧱 Build; 📐 Resize & nest; ♻️ Fork |
| 03 | 🤖 Agentic Fleet | 🤖 Agents; 📧 Robot-to-robot email; 📋 Kænbæn; 🧾 Witness |
| 04 | 🏙️ Public Worlds | 🌐 Destinations; 📦 GitHub; 🔗 æQR; ❤️ Return value |

Inside any frame, offer MoW selection and nested MoW composition, e.g. Agent Fleet may contain a mail widget alongside a chat widget, each with its own child drawers. Illustrative controls must not claim that Gmail, GitHub publishing, Code execution, commerce or agent runtimes are connected unless verified.

## Release boundaries / continuity

- The **ChatGPT conversation cockpit** and existing **æ Studio OpenAI Site** remain **peer destinations**, neither replacing the other. GitHub is versioned engineering source, not a substitute for either.
- Reuse current `index.html`, `mcp/`, `mcp/agents/`, `mcp/discover/`, `mcp/kinetic/`, æQR, existing Site and `ae-destinations.json`. Avoid duplicate site and wholesale rewrite.
- Publication requires deliberate human review. A saved architecture record, feature-branch commit, UI preview, tests, merged pull request, and actual deployment are **different states**.
- No secret context, tokens, user-specific Gmail content, permission grants, or private session histories in public manifests.
- No actual robot-to-robot email sent by rendering its widget; no external code run or transaction from clicking a demo surface.

## Suggested implementation slice

1. Create a reusable `ae-carousel` scene renderer, `ae-drawer`, `ae-widget`, and `ae-mixture` state schema; do not replace the existing atlas.
2. Implement an accessible 9:16 **full-scene carousel** with a navigable set of drawer hosts. Give child widgets stable identity and keyboard/focus support.
3. Implement a MoW selector with nested mixtures, preserving independent child state and avoiding duplicate event propagation.
4. Check responsive scaling, reduced-motion and motion pause, touch/swipe, recursive-depth guardrails, URL/reference identity, and side-effect gating.
5. Demonstrate one read-only integration with source revision and honest capability state before connecting execution providers.
6. Review branch diff and secure explicit separate approval before merge or deploy.

**North star:** Many widgets. Many agents. One human principal. **Return value to the human. ❤️**
