# æ protocol — the protocol of agentic environments

**Site name:** æ protocol
**One line:** the protocol of agentic environments.
**Operator:** Yæl Méndez · one person · one estate · many agents.

The estate's address stays `myaelmendez.github.io`; the *name of the thing* is æ protocol.
An address is where it lives. A name is what it is.

---

## 1. What æ protocol is

Not a product page. Not a portfolio. It is **the surface that shows how a sovereign agent
estate is built**, published as a working instrument.

Three names, three jobs — keep them apart:

| name | job |
|---|---|
| **`yæl`** | the kernel of the operator console |
| **`mæch`** | the development language |
| **`æ`** | the agentic electronic language for machine-learning programming |

The console *runs* yæl, is *written* in mæch, and *speaks* æ.

---

## 2. The white-label standard

White-labelling is not a feature bolted onto the homepage. **It is the default posture of
every surface**: the estate is the pattern, the visitor wears it.

### Contract

Every surface that renders an identity slot carries these inputs:

| field | meaning | stored |
|---|---|---|
| `glyph` | the visitor's mark (≤2 chars, free text or an image) | `localStorage['ae-label-v1']` |
| `name` | their venture / project name | same |
| `accent` | their colour, driving `--gold`/`--gold-hi` | same |

Rules, non-negotiable:

1. **Nothing defaults to æ.** æ is the operator's. An empty label means the surface is wearing
   its own demo face, never a borrowed one.
2. **The label is data, not code.** It lives in one shared module
   (`assets/brand/ae-label.js`), included by every surface — never copy-pasted per page.
3. **The label styles; it does not rewrite content.** It sets variables and swaps identity
   slots. It never rewrites the estate's facts, receipts or numbers.
4. **Shipping is a fork.** A visitor's browser wearing the surface is a *preview*. Making it
   theirs means forking the repository — the page says so when it says anything at all.

### Required identity slots

`<body data-label-glyph>`, `<body data-label-name>` — a surface fills these if it has a face.
A surface without them simply inherits the variables.

---

## 3. The teaching path — the surface is the sample

People learn by *doing as we do*, not by reading about it. So every mechanism ships three ways
at once:

| layer | what the learner gets |
|---|---|
| **wear it** | click, set a glyph, see the whole surface re-skin |
| **read it** | the mechanism's own spec, on the surface itself (`>_æ://…/*.md` rendered as æ-surfaces) |
| **fork it** | the repository, with the mechanism intact and commented |

Nothing in the estate is presented without its receipt, and nothing is receipted without being
inspectable. **The sample is the documentation.**

---

## 4. Fork · clone · contribute

| step | what happens |
|---|---|
| **fork** | take the whole estate as a template — the console, the store, the pet, the label |
| **clone** | run it locally; the receipts reproduce because the pipeline is deterministic |
| **contribute** | a contributed mechanism must carry: an artifact, a receipt, a continuity entry, and a gate that fails |

The bar for contribution is the bar the estate already holds itself to: **a claim that has not
been checked back is not a thing.**

---

## 5. The funnel

```
1  Nous Portal subscription        → the compute exists
2  install Hermes Agent            → the agent exists
3  point their agent at the estate → the loop closes
```

Step 1 is why the referral matters: it funds the leaf that makes every later step runnable.
Step 2 gives the learner an agent that can read the surface, not just render it.
Step 3 is the intent of the whole design — *point your agent at me*.

Every surface that asks for anything asks in that order, and says why.

---

## 6. Honest state

- White-labelling today lives on `index.html`; the shared module makes it standard. Surfaces
  without identity slots are unaffected.
- The console runs yæl and speaks æ; it has no execution path yet — plans and receipts only,
  until the conductor bridge lands.
- Nothing here claims adoption. It claims a pattern, shown working.
