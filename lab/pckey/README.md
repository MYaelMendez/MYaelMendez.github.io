# pc://key · PrivateClient owner key + væult

Live on node^0 at https://privateclient.ai/key/ (stdlib Python, `pckey.py`, 127.0.0.1:8791).

- **Face ID = authority (æ2).** The owner enrolls with WebAuthn (ES256, user verification required). The first device needs a single-use enroll token; each extra device needs an unlocked session.
- **The væult is end to end.** Secrets are encrypted on the device with AES-GCM-256. The key comes from HKDF over the passkey's WebAuthn PRF output, and the secret's name is bound as AAD. node^0 stores only ciphertext and rejects anything that isn't base64url. There is no PRF fallback: without PRF the væult stays shut.
- **Sessions:** 10 min, HttpOnly + Secure + SameSite=Strict cookie, and an Origin check.
- **📟 Witness:** a hash-chained log of enroll, unlock, put, reveal, delete and refused events. It records names only, never values.
- Doctrine: Many agents. One principal. Context may propagate; authority does not.
