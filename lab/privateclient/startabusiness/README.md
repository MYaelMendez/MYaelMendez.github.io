# #startabusiness / · LAB mirror

Mirror of the LIVE page https://privateclient.ai/startabusiness (deployed 2026-10-19, approved by Yæl for this change).

- Three doors: **privateclient.ai | CLI.LLC | DAOLLC.AI**, formation partner **doola**.
- Primary CTA → doola PartnerStack link `https://partnersps.doola.com/hhsoqhb23250` (`target=_blank`, `rel="noopener sponsored"`).
- Live home (`/`) has one yellow button `#startabusiness /` (#f5c400, black text, ≥44px, same label in EN/ES/PT/FR/DE/SV) → `/startabusiness`.
- **Pending:** doola embedded partner iframe. Set `DOOLA_PARTNER_EMBED_ID` (one constant in the page script) once doola confirms the production partner ID → renders `https://app.doola.com/embed/partner/<ID>`. Live route CSP already allows `frame-src https://app.doola.com`. Do not invent an ID.
- Paths: ① referral (live) · ② embed (slot) · ③ partner API (later). Track conversion by verified settlement, not clicks.

LAB copy differs from live only by `noindex` and absolute links back to privateclient.ai.

>_ Many agents. One principal.
