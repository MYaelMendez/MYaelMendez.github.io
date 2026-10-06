# Prior-Art Review: The Physical Air-Gap Paper

**Date:** 2026-10-06
**Subject:** `papers/physical-airgap-envelope.md`
**Verdict:** The paper's novelty claim **does not survive** as written. It must be narrowed.

---

## Summary

The paper claims, twice, "we are not aware of prior work that treats the envelope format itself as the object of design across multiple physical and network transports." A literature search finds that claim is **false as stated**. The core property the paper presents as its contribution — *a secret can be disseminated over public channels such that anyone who scans it obtains only ciphertext* — was published in 2018.[2]

The paper is still publishable, but the contribution must be **repositioned** from "we invented a typed envelope for sovereign transport" to "we specify, implement, and physically evaluate a single envelope across three transports, and report a scan-time failure class." That is a narrower, defensible claim.

---

## Finding 1: The core property is prior art (2018)

Chow, Susilo, Tonien, Vlahu-Gjorgievska, and Yang, "Cooperative Secret Sharing Using QR Codes and Symmetric Keys," *Symmetry* 10(4):95, April 2018.[2] From the abstract:

> "The advantage of this approach is that the shares can be disseminated over public channels, as anyone who scans the QR codes will only obtain public information. Only authorized individuals who are in possession of the required keys will be able to recover the shares."[2]

This is **the same invariant** the paper states as its central contribution ("possession of the transport must not imply possession of the secret"). The paper does not cite it. This is the most serious finding.

What [2] adds that the paper does not have: **secret sharing** (Shamir-style threshold schemes), where a secret is divided among *n* participants and recovered by *k* cooperating holders. The paper's envelope is single-key, single-recipient. That is a genuine difference — but it is a *weaker* property, not a novel one.

## Finding 2: The "typed envelope" is standardised practice (EMV)

EMVCo maintains the EMV QR Code Specifications, a standardised template for payment QR codes.[3] It is a typed, self-describing payload with a versioned schema, maintained as a standard with conformance tooling.[3] The paper's claim that treating the envelope format as a design object is novel is not sustainable against a decade of EMV practice.

What the paper's envelope has that EMV does not: it is **symmetric-key sealed** and **transport-agnostic by design**. EMV is a payment-specific schema for a single transport (scan-at-checkout). That distinction is real but narrower than the paper claims.

## Finding 3: QR secret distribution is an active subfield

Additional prior work found:

- A lossless-recovery secret distribution scheme based on QR codes, *Entropy* 25(4):653, 2023.[1] — addresses QR capacity limits and lossless recovery, which overlaps the paper's segmentation concern.
- `skewthreads/QR-secret-sharing` — a public, starred implementation of QR secret sharing.[5]

The existence of an active subfield means the paper's Related Work section is materially incomplete, not merely thin.

### An unverifiable lead

A search result titled "Performance Limits of QR Code Technology for Air-Gapped Military Transfer" (DiVA thesis, `diva2:1878420`) appeared to directly study the physical transfer channel the paper evaluates. **I could not retrieve it** — the host serves an Anubis proof-of-work bot wall, and extraction returned the challenge page, not the document. It is therefore **not cited** anywhere in this review. If it is as relevant as its title suggests, it likely contains capacity/throughput measurements that would supersede the paper's informal QR version analysis. This is flagged as a lead for manual follow-up, not as evidence.

---

## What survives

After the prior-art review, the paper's defensible contributions are:

| Claim | Status |
|---|---|
| A typed 8-type envelope for sovereign transport | **Not novel** — EMV standardises typed QR payloads[3] |
| Secrets disseminated publicly yield only ciphertext | **Not novel** — published 2018[2] |
| One envelope across email + SMS + QR | **Narrowly novel** — [2] is QR-only; [3] is payment-only. Cross-transport uniformity is not claimed in either. |
| SMS segmentation with self-describing chunk markers | **Narrowly novel** — [2] does not address SMS; [1] addresses QR capacity, not SMS segments |
| The verify-before-store import protocol | **Plausibly novel as a named protocol** — but the *practice* (decrypt before accepting) is standard hygiene, so the novelty is in the specification, not the idea |
| The non-ASCII magic scan failure (§5.3) | **Genuinely novel as a reported result** — no prior source found describing this failure class |
| Physical evaluation of 8 types through pyzbar | **Incrementally novel** — an evaluation contribution, not a design contribution |

---

## Required changes to the paper

1. **Delete both "we are not aware of prior work" sentences.** Replace with an accurate Related Work section citing [1]–[5].
2. **Reposition the contribution.** From "we present a typed envelope" to "we specify, implement, and physically evaluate a single envelope across three transports, and report a scan-time charset failure class."
3. **Cite [2] explicitly** as the source of the public-channel ciphertext property, and state what the paper adds beyond it (cross-transport uniformity, verify-before-store, the negative result).
4. **Cite [3]** and concede that typed QR payloads are standardised.
5. **Strengthen §5.3** — it is now the paper's strongest novel claim and deserves more than one subsection.
6. **Re-title if necessary.** "A Typed Envelope" overclaims. Something like "One Envelope, Three Transports: Physical Evaluation of a Cross-Transport Secret Format" is honest.

---

## Method note

Sources were retrieved with `web_search` + `web_extract`, registered in a citation ledger, and evidence quotes were attached and **verbatim-verified against the extracted page text** (the quote is rejected unless it appears in the fetched text). This finding was produced because the paper's novelty claim was checked rather than assumed — the search took five queries.

---

## Sources

[1] https://pmc.ncbi.nlm.nih.gov/articles/PMC10137899 — A Lossless-Recovery Secret Distribution Scheme Based on QR Codes
[2] https://www.mdpi.com/2073-8994/10/4/95 — Cooperative Secret Sharing Using QR Codes and Symmetric Keys
    > "The advantage of this approach is that the shares can be disseminated over public channels, as anyone who scans the QR codes will only obtain public information. Only authorized individuals who are in possession of the required keys will be able to recover the shares."
    > "Secret sharing is an information security technique where a dealer divides a secret into a collection of shares and distributes these to members of a group."
[3] https://www.emvco.com/emv-technologies/qr-codes — EMV QR Code Specification
    > "The EMV QR Code Specifications provide a standardised template for the generation of QR codes that will work consistently everywhere to deliver convenient and reliable card and account-based payments."
    > "EMVCo maintains the EMV QR Code Specifications, supporting self-evaluation tools, and EMV QR Marks."
[5] https://github.com/skewthreads/QR-secret-sharing — QR-secret-sharing implementation
    > "skewthreads/ QR-secret-sharing Public"

**Not cited (could not verify):** `diva2:1878420` — host serves a bot wall; see "An unverifiable lead" above.
