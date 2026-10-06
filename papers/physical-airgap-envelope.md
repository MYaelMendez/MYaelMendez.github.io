# The Physical Air-Gap: A Typed Envelope for Sovereign Secret Transport

**Yæl Méndez**
Independent Researcher
`yael@llm.store`

---

## Abstract

Cloud secret managers make a structural bet: that the custodian of the secret is trustworthy. Every major commercial system (HashiCorp Vault, AWS Secrets Manager, Doppler, 1Password) requires the secret to exist on infrastructure the operator does not control, and every network transport for secrets — email, SMS, chat — carries the secret in a form that a reader of that transport can recover. We present a different design: a **typed, self-describing envelope** that carries only AEAD ciphertext, and a **transport-agnostic import protocol** that proves a received blob opens under the local key before storing it.

The central artifact is an eight-type envelope with a single ASCII magic (`ae:1:<type>:<b64url(json)>`) that encodes keys, sealed secrets, contracts, capability grants, routes, agent handoffs, identities, and surface manifests in one wire format. We show empirically that (1) all eight types survive a **physical** encode → print → scan → decode loop through pyzbar; (2) a 659-byte sealed secret segments into six 160-character SMS parts that reassemble byte-exactly; (3) email messages carrying the envelope in both the body and a QR attachment yield zero plaintext bytes while remaining importable; and (4) a non-ASCII magic (`æ:`) **generates correctly but fails on scan** — a silent failure class that only the physical loop detects.

The contribution is not a new cipher but a **transport discipline**: possession of the transport must never imply possession of the secret. We argue this property, not key strength, is what makes email and SMS usable in a sovereign stack, and we release the envelope, the vault, and the transports as open sourceware.

---

## 1. Introduction

Secret management today is a custody question disguised as a cryptography question. AES-256-GCM is not the hard part; the hard part is that the standard answer to "where does the key live?" is "somewhere you don't control." HashiCorp Vault, AWS Secrets Manager, Doppler, and 1Password all place the secret on remote infrastructure and ask the operator to trust an access-control model. That model is appropriate for a fifty-person team with compliance obligations. It is a poor fit for a **one-person company** whose threat model is "the cloud is a place my secrets can leak."

The consequence of the cloud-first model is that the *transport* becomes an afterthought. A secret sent by email sits in the body as plaintext — in the sender's outbox, in SMTP logs, in the recipient's inbox forever. A secret sent by SMS sits in a carrier's database. Both transports are *readable by parties who are not the intended recipient*, and both are therefore unusable for anything that matters. The industry's answer is "don't send secrets by email," which is a prohibition rather than a design.

We take the opposite approach. If the transport is untrusted, then the transport must carry **ciphertext only**, and the receiver must be able to *verify* that a received blob is openable under their key before accepting it. This paper specifies such a design and evaluates it on the physical medium.

### 1.1 Contributions

- **A typed envelope.** One wire format (`ae:1:<type>:<b64url(json)>`) for eight payload classes: `key`, `secret`, `contract`, `capability`, `route`, `handoff`, `identity`, `manifest`. The type is in the clear so a scanner dispatches without guessing; the payload is base64url JSON so it survives QR alphanumeric mode.
- **A verify-before-store import protocol.** Every receive path decrypts the blob under the local key and refuses to store on failure. A message sealed under a different passphrase is skipped, never imported.
- **A physical evaluation.** We test all eight types through a real print-and-scan loop (encode → PNG → pyzbar → decode), not merely in memory.
- **A segmentation scheme for SMS.** A 659-byte envelope splits into six parts with a self-describing chunk marker (`ae:1:<type>:chunk:<i>/<n>:<part>`) that reassembles byte-exactly.
- **A negative result.** A non-ASCII magic generates correctly and **fails on scan**; we characterize the failure and the fix.

### 1.2 The property we are buying

> **Possession of the transport must not imply possession of the secret.**

Everything below is in service of that one invariant. It is what makes email and SMS admissible, and it is what a cloud secret manager does *not* provide, because in a cloud manager the transport (the vendor's API) and the secret are the same custody domain.

---

## 2. Related Work

**Password-based key derivation.** scrypt [1] and PBKDF2 [2] are the two memory-hard and iterated KDFs we support. Both are used unchanged; our contribution is not in the KDF but in the envelope that carries the derived-key ciphertext. We note that the two functions differ in their parameter space and that a single vault file must therefore carry its KDF identifier — a point we return to in §3.2.

**Authenticated encryption.** AES-256-GCM [3] provides the confidentiality and integrity we rely on. Our use is standard except for one detail: the entry name is bound into the AEAD's associated data, so a renamed or swapped entry fails to decrypt rather than silently yielding the wrong plaintext.

**Structured token formats.** JSON Web Signature [4] is the closest well-known antecedent to our envelope: a base64url JSON payload with a cleartext header. We differ in two ways that matter for this application. First, JWS is designed for *signed* tokens verified by a public key, whereas our envelope is designed for *sealed* payloads opened by a shared passphrase — a symmetric, offline setting. Second, JWS has no notion of a physical transport; our envelope is sized and encoded for QR alphanumeric mode and SMS segments.

**Physical transports.** QR codes have been used for offline key transfer (e.g., paper backups of PGP keys). Base64 and base32 encodings [5] are the standard alphabets for that transfer. We are not aware of prior work that treats the **envelope format itself** as the object of design across multiple physical and network transports, or that reports the scan-time charset failure we describe in §5.3.

**Signature and KDF primitives for the key type.** Ed25519 [6] and HKDF [7] are used in the `key` envelope type; TLS 1.3 [8] is the transport we deliberately do *not* require, since the design assumes the transport is hostile.

---

## 3. Design

### 3.1 The envelope

```
ae:1:<type>:<b64url(json)>
```

| Field | Purpose |
|---|---|
| `ae:` | magic — **ASCII**, chosen for scan-safety (§5.3) |
| `1` | envelope version |
| `<type>` | one of eight payload classes, in the clear |
| `<b64url(json)>` | payload, base64url, unpadded |

The type is cleartext so that a receiver can dispatch without decrypting. This is a deliberate trade: it leaks *what kind* of object is in transit (a key vs. a secret vs. a manifest) but never *what it contains*. For our threat model this is correct — the adversary who reads the transport learns "a sealed secret is here," which they already knew, and nothing more.

### 3.2 The eight types

| Type | Payload | Sealed? |
|---|---|---|
| `key` | Ed25519/RSA keypair | no (paper backup; the QR *is* the key) |
| `secret` | `{name, blob:{n, ct}}` | **yes** |
| `contract` | `{type, parties, hash, ...}` | no |
| `capability` | `{grant, subject, expires}` | **yes** |
| `route` | `{cmd}` | no |
| `handoff` | `{from, to, kind, ...}` | no |
| `identity` | `{node, public_key, host}` | no |
| `manifest` | `{base_url, surfaces}` | no |

The `secret` type is the load-bearing one. Its `blob` is exactly what the vault stores: a 96-bit nonce `n` and a GCM ciphertext `ct` whose associated data is `vault-entry:<name>`. The envelope does not re-encrypt; it *carries* the vault's sealed form. This is what allows a secret to move between machines without ever existing as plaintext outside a running process.

### 3.3 Verify-before-store

The receive path is the security-critical one:

```
for each envelope in message:
    kind, payload = decode(envelope)
    if kind != "secret": continue
    value = open_entry(local_key, payload.name, payload.blob)
        on failure: SKIP          # sealed under a different passphrase
    store(payload.name, payload.blob)
```

The `open_entry` call is the gate. It is not a heuristic or a format check — it is a real AEAD decryption under the receiver's derived key. A blob sealed under a different passphrase raises, and the message is skipped. This is why a leaked mailbox is harmless: the attacker has the ciphertext and the name, and neither is enough.

### 3.4 Transport adapters

The envelope is transport-independent. We implement three:

**Email.** The message body carries the envelope as text, and optionally the same envelope is attached as a QR PNG. A receiver imports from either. The `.eml` can be decoded offline with no credentials, which lets an operator verify a message before wiring IMAP.

**SMS.** The 160-character GSM-7 limit forces segmentation. An envelope longer than one segment is split into `ae:1:<type>:chunk:<i>/<n>:<part>` parts. The chunk marker is itself a valid envelope prefix, so the receiver parses uniformly. `reassemble()` sorts by index and concatenates, refusing on an incomplete set.

**QR.** The canonical physical transport: render the envelope to a PNG, print it, scan it. The QR carries the same bytes as the network transports, so a secret can cross from a network context to an air-gapped one without re-encoding.

---

## 4. Implementation

We release three artifacts, all open sourceware:

| Artifact | Role | Size |
|---|---|---|
| `qr_envelope.py` | the codec + CLI | 7 KB |
| `qr_mail.py` | email transport | 13 KB |
| `qr_sms.py` | SMS transport + segmentation | 14 KB |

The codec has no dependencies beyond the standard library. The transports depend on `qrcode`, `pillow`, and `pyzbar` for rendering and scanning.

A conductor scheme exposes the codec as `qr://` with actions `types`, `encode`, `decode`, `inspect`, `png`, and `read`, and the vault scheme exposes `væult://email-import` and `væult://sms-import`. The `inspect` action returns type, version, field names, and byte count **without payload values**, so it is safe to log.

---

## 5. Evaluation

### 5.1 Physical air-gap survival

We test all eight types through the full physical loop: `encode` → render to PNG → scan with pyzbar → `decode` → compare. This is the only test that exercises a real decoder; an in-memory round trip does not.

**Table 1: Physical round-trip survival (encode → PNG → pyzbar → decode).**

| Type | QR version | Envelope bytes | Scanned type | Payload match |
|---|---|---|---|---|
| `secret` | v6 | 86 | secret | ✓ |
| `route` | v4 | 46 | route | ✓ |
| `capability` | v7 | 116 | capability | ✓ |
| `key` | v13 | 288 | key | ✓ |
| `contract` | v6 | 101 | contract | ✓ |
| `handoff` | v5 | 77 | handoff | ✓ |
| `identity` | v9 | 166 | identity | ✓ |
| `manifest` | v7 | 110 | manifest | ✓ |

**8/8 types survive the physical loop.** All fit within QR version 40 (the cap is approximately 2.9 KB).

### 5.2 SMS segmentation

A 659-byte sealed secret (a 300-character value under a fresh nonce) is segmented and reassembled:

**Table 2: SMS segmentation of a 659-byte envelope.**

| Property | Value |
|---|---|
| envelope bytes | 659 |
| segments | 6 |
| chars per segment | 151 (≤ 153 limit) |
| reassembly | byte-exact (`rebuilt == env`) |
| post-reassembly open | succeeds, value matches |

The chunk marker costs 24 characters per segment (`ae:1:secret:chunk:2/6:`), which is why the effective payload is 153 rather than 160. The 24-character overhead is the price of self-describing chunks; the alternative — positional reassembly — requires the receiver to know the message boundaries, which SMS does not provide.

A short secret (134-byte envelope, e.g. a Wi-Fi password) fits a single segment with no overhead; a mid-length secret (147-byte envelope) also fits one segment.

### 5.3 The non-ASCII magic failure (negative result)

Our first design used the rune `æ:` as the magic, matching the project's identity. It **generates correctly and fails on scan**:

```
original: 'æ:1:secret:...'      U+00E6        (UTF-8: C3 A6)
scanned : 'ﾃｦ:1:secret:...'     U+FF83 U+FFA6 (halfwidth katakana)
```

pyzbar re-interprets the two UTF-8 bytes of `æ` as two halfwidth-katakana characters. The decoder returns a string that is visually similar and byte-different, and `is_envelope()` returns false. Crucially, **an in-memory `encode → decode` round trip passes** — the failure appears only when a real decoder is in the loop.

We characterize this as a *silent failure class*: the encoder is correct, the payload is correct, the QR renders, and the receiving application rejects valid traffic. The fix is to make the magic ASCII (`ae:`) and to accept the rune form on decode for backward compatibility. We report this because the general lesson — **test through the real decoder, not an in-memory shim** — is cheap to state and expensive to learn.

### 5.4 Email plaintext audit

We construct a real `EmailMessage` with the envelope in the body and the QR PNG attached, serialize it to `.eml` bytes, and search for the plaintext value:

**Table 3: Plaintext audit of an email carrying a sealed secret** (value `mi-api-key-9876`, sealed under a real vault key).

| Artifact | Size | Contains plaintext? |
|---|---|---|
| envelope string | 147 B | **no** |
| `.eml` bytes (body + QR) | 2,701 B | **no** |
| envelopes found on decode | 2 (body + QR) | — |
| both open under the vault key | yes | — |

Both the body path and the QR-attachment path recover the same value. Neither contains the plaintext. (The 147-byte envelope here carries a real sealed value; the 86-byte `secret` row in Table 1 uses a synthetic sample blob of the same shape, so the two are not directly comparable in size.)

### 5.5 Failure behavior

The system fails closed on every malformed input we tested:

**Table 4: Rejection behavior.**

| Input | Result |
|---|---|
| `hello world` | rejected — missing magic |
| `ae:1:bogus:zzz` | rejected — unknown type |
| `ae:9:secret:zzz` | rejected — unsupported version |
| `ae:1:secret:!!!` | rejected — corrupt payload |
| blob sealed under a different passphrase | skipped at import |
| vault locked (no passphrase) | import refused |

---

## 6. Discussion

### 6.1 Why the envelope, not the cipher, is the contribution

Every primitive here is standard: scrypt, PBKDF2, AES-GCM, Ed25519, base64url. A reader looking for novelty in the cryptography will not find it. The novelty is in **where the plaintext is allowed to exist** and **what the receiver checks before accepting**. The envelope makes the transport uniformly hostile by ensuring no transport ever sees a plaintext value; the verify-before-store protocol makes the receiver active rather than credulous.

### 6.2 The cloud-manager comparison, stated fairly

A cloud secret manager provides capabilities this design does not: role-based access control, audit logs, automatic rotation, dynamic short-lived credentials, and multi-region availability. For a team with compliance obligations, those are requirements and this design is insufficient. The claim is narrower: for a single operator whose threat model is *custody*, a local vault plus a ciphertext-only envelope is a better fit, because it removes the trusted third party entirely rather than asking the operator to trust one carefully.

### 6.3 Limitations

**The passphrase is the single point of failure.** It cannot live inside the vault (chicken-and-egg), and both sender and receiver must hold the same one. We provide no key-exchange protocol; the passphrase is a shared secret established out of band. This is a real limitation, and the honest framing is that the design relocates trust rather than eliminating it.

**The vault file is a single point of failure.** It is one file on one disk. A backup is a file copy and is encrypted, so a backup is safe to store anywhere — but the operator must actually make one, and we do not automate that.

**No forward secrecy.** A compromised passphrase decrypts every envelope ever sent, because the same derived key protects all of them. Rotating the passphrase requires re-sealing entries. We do not implement rotation.

**Segmentation assumes in-order delivery per message.** Our `reassemble()` sorts by chunk index, so out-of-order *arrival* is handled, but chunks from two different messages interleaved into one input would be merged. The current implementation mitigates this by grouping per message at the transport layer; the codec itself does not carry a message identifier.

**No formal verification.** We test empirically and report the results; we do not provide a proof of the envelope's soundness or a mechanized analysis of the protocol.

**The physical loop was tested with pyzbar, not a phone camera.** Our scan tests use pyzbar on rendered PNGs. A phone camera introduces lighting, angle, and lens distortion that our tests do not model. We expect the ASCII magic to be robust (that was the point) but we have not measured camera-path success rates.

---

## 7. Conclusion

We presented a typed envelope and a verify-before-store import protocol that make email, SMS, and paper admissible transports for secrets, on the invariant that **possession of the transport must not imply possession of the secret**. All eight envelope types survive a physical print-and-scan loop; a 659-byte secret segments into six SMS parts and reassembles byte-exactly; an email carrying the envelope in body and QR attachment contains zero plaintext bytes while remaining importable. We also report a negative result: a non-ASCII magic generates correctly and fails on scan, a silent failure class that only a real decoder exposes.

The broader claim is that for a sovereign operator, the interesting design work in secret management is not the cipher but the **transport discipline** — and that a single, typed, self-describing envelope is a practical way to impose it across heterogeneous media.

All artifacts are released as open sourceware. The tool is open; the secrets are not.

---

## References

[1] C. Percival and S. Josefsson, "The scrypt Password-Based Key Derivation Function," RFC 7914, Aug. 2016. doi:10.17487/RFC7914.

[2] B. Kaliski, A. Rusch, and K. Moriarty, Ed., "PKCS #5: Password-Based Cryptography Specification Version 2.1," RFC 8018, Jan. 2017. doi:10.17487/RFC8018.

[3] M. J. Dworkin, "Recommendation for block cipher modes of operation: Galois/Counter Mode (GCM) and GMAC," NIST Special Publication 800-38D, 2007. doi:10.6028/NIST.SP.800-38D.

[4] M. Jones, J. Bradley, and N. Sakimura, "JSON Web Signature (JWS)," RFC 7515, May 2015. doi:10.17487/RFC7515.

[5] S. Josefsson, "The Base16, Base32, and Base64 Data Encodings," RFC 4648, Oct. 2006. doi:10.17487/RFC4648.

[6] S. Josefsson and I. Liusvaara, "Edwards-Curve Digital Signature Algorithm (EdDSA)," RFC 8032, Jan. 2017. doi:10.17487/RFC8032.

[7] H. Krawczyk and P. Eronen, "HMAC-based Extract-and-Expand Key Derivation Function (HKDF)," RFC 5869, May 2010. doi:10.17487/RFC5869.

[8] E. Rescorla, "The Transport Layer Security (TLS) Protocol Version 1.3," RFC 8446, Aug. 2018. doi:10.17487/RFC8446.

---

## Appendix A: Reproducing the results

```bash
# 1. the codec round-trips every type in memory
python -c "from qr_envelope import *; [decode(encode(t, {})) for t in TYPES]"

# 2. the PHYSICAL loop (this is the test that matters)
python - <<'EOF'
from qr_envelope import encode, decode, is_envelope
import qrcode
from pyzbar.pyzbar import decode as zbar
from PIL import Image
env = encode("secret", {"name": "K", "blob": {"n": "a", "ct": "b"}})
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=2)
qr.add_data(env); qr.make(fit=True)
qr.make_image(fill_color="black", back_color="white").save("t.png")
scanned = zbar(Image.open("t.png"))[0].data.decode()
assert is_envelope(scanned), "the magic did not survive the scan"
assert decode(scanned)[0] == "secret"
print("physical loop OK")
EOF

# 3. SMS segmentation is byte-exact
python -c "import qr_sms, qr_envelope as qe; e=qe.encode('secret',{'name':'K','blob':{'n':'a','ct':'b'}}); assert qr_sms.reassemble(qr_sms.segments(e))==e"

# 4. no plaintext in a mailed envelope
qr_mail.py decode message.eml    # inspect: the payload must be a blob
```

## Appendix B: The eight types, by example

```
ae:1:secret:eyJuYW1lIjoiWElBT01JIiw...   {name, blob:{n, ct}}
ae:1:route:eyJjbWQiOiJ2w6Z1bHQ6Ly8gc...   {cmd: "væult:// status"}
ae:1:key:eyJhbGdvcml0aG0iOiJlZDI1NTE5...  {algorithm, public_key, private_key, fingerprint}
ae:1:capability:eyJncmFudCI6ImdwdTptYX...  {grant, subject, expires}
ae:1:contract:eyJ0eXBlIjoiZXNjcm93Iiw...   {type, parties, hash}
ae:1:handoff:eyJmcm9tIjoidmljdHVzIiw...    {from, to, kind}
ae:1:identity:eyJub2RlIjoidmljdHVzIiw...   {node, public_key, host}
ae:1:manifest:eyJiYXNlX3VybCI6Imh0dHB...   {base_url, surfaces}
```
