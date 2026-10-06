# QR is itself open sourceware

**The observation:** our entire QR strategy — vault export, air-gap transfer, mail,
SMS, the kanban machine — rests on a substrate that is itself free to use. That is
not incidental. It is the reason the stack is sovereign.

## The verified position

DENSO WAVE invented the QR code in 1994 and holds the patents. Their published
position is that they do not exercise them for standard use:

> "DENSO WAVE INCORPORATED has a number of patents on QR Code."[6]

> "**Everyone can use the QR Code freely as long as following the standards for QR
> Codes in JIS or ISO.**"[6]

> "If you are considering using a QR Code that deviates from the standards, please
> contact the patent holders before using the code."[6]

And the symbology is standardised: ISO/IEC 18004 defines the QR Code symbology.[7]

## The precise boundary

This is the part worth being exact about, because "QR is free" is repeated loosely
and the actual grant has a condition:

| Use | Status |
|---|---|
| Standard QR (ISO/IEC 18004 / JIS X 0510) | **free** — "everyone can use... freely"[6] |
| A QR that **deviates from the standards** | contact the patent holders first[6] |

So the freedom is *conditional on conformity*. It is not "the patent is abandoned";
it is "the patent is not exercised against conformant use." Those are different
claims, and only the second is what DENSO actually says.

**Our stack is conformant.** We use standard QR, model 2, with the standard
alphanumeric/byte modes and standard error-correction levels. We do not modify the
symbology. We layer *on top of* it.

## Why this matters for the æ:// stack

The layering is the whole design, and it is what makes the substrate choice correct:

```
ISO/IEC 18004  →  the symbology        free to use, conformant[6][7]
qrcode/pyzbar  →  the encoder/decoder  open source (MIT/BSD)
ae:1:<type>:   →  OUR envelope          MIT, ours
væult          →  OUR sealing           MIT, ours
```

Every layer below ours is free and open. That means:

1. **No royalty can be extracted from the pipeline.** Nothing in the chain from
   `encode()` to a printed card carries a licence fee.
2. **No vendor can revoke the transport.** The symbology is standardised and the
   grant is public; a QR card printed today scans in ten years.
3. **The physical medium is unownable.** Paper, ink, a camera. There is no API to
   deprecate and no account to suspend.

Contrast with the transports we deliberately did *not* build on: a cloud secret
manager's API, a proprietary token format, a vendor's scan SDK. Each of those is a
layer someone else controls, and each can be repriced or switched off.

## The rule this establishes

> **Build the transport on a substrate nobody can charge for, and put your own
> contribution on top of it.**

The QR substrate is free and conformant.[6][7] The envelope is ours and MIT. The
sealing is ours and MIT. That is a stack with no rent collector anywhere in it.

It is the same move as the rest of æ://: the namespace is the contribution, the
substrate is a commons.

## Sources

[6] https://www.qrcode.com/en/patent.html — About the patent, DENSO WAVE
    > "DENSO WAVE INCORPORATED has a number of patents on QR Code."
    > "Everyone can use the QR Code freely as long as following the standards for QR Codes in JIS or ISO."
    > "If you are considering using a QR Code that deviates from the standards, please contact the patent holders before using the code."
[7] https://www.iso.org/standard/62021.html — ISO/IEC 18004:2015, QR Code symbology
