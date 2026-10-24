# Preserved origin

The former root homepage from `7befaf5dafce517393261d5b4bb50f9b0e679cee` now lives at `/origin/`. Its atlas, terminal, mesh, theme/environment controls, announcements and onboarding destinations are retained.

Compatibility changes: a `base href="../"` keeps the original root assets and relative destinations working; canonical/social URL points to `/origin/`; a return link opens the new homepage; the DOM helper is declared before its first use, fixing the pre-existing `$ is not a function` startup error. No other application logic is rewritten. The original source remains retrievable at that Git commit.

The old terminal contains historical demonstration status strings. Moving it does not verify those claims, register a protocol, connect models or grant authority. The new homepage reports the implemented local tools explicitly.
