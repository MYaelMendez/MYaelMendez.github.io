# æ markers · gates (LAB)

The agent writes markers like `[[ask: title | detail]]`. **A marker is a request; the gate decides.** The table is in `markers.json` (`ae.markers/0.1`).

- Unknown markers are refused (default deny), and the refusal is witnessed.
- `status`, `step`, `notify` are allowed at æ0. `output` is allowed only inside `outputs/`. `done` moves a card to review, and only Yæl moves it to done.
- `ask`, `pay`, `schedule`, `publish` are æ2 and human_only, single use, expiring after 120 s.
- `login` and `handoff` are æ3. The vault fills secrets by id and the agent never sees them. On a handoff the agent stops and the human acts.
- Every decision writes a SHA-256 chained Witness receipt, and tampering breaks the chain.

Inspired by the marker pattern in Cua Bots (trycua/cua), whose README says its rules are guidance and not enforcement. Here they are enforced. This is our own implementation and contains no Cua code (that sample is FSL-1.1-MIT).

LAB only, simulated. #OPENSOURCEWARE · Many agents. One principal.
