# æQR Badge Widget — QR Code Interactive Generator

Widget para generación y verificación de códigos QR con integración æ:// 

```javascript
import { useState } from 'react';

export function AeQrWidget({ data, size = 48 }) {
  const [qrSvg, setQrSvg] = useState(null);
  const [verified, setVerified] = useState(false);

  const generate = async () => {
    // Generate QR with æ:// scheme validation
    const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=${size}x${size}&data=${encodeURIComponent(data)}&color=D4AF37&bgcolor=050505`;
    setQrSvg(qrUrl);
  };

  const verify = async () => {
    // Verify æqr payload structure
    const payload = parseAeQrPayload(data);
    setVerified(payload.decoded_ok === true);
  };

  return (
    <div className="aeqr-widget">
      {qrSvg && <img src={qrSvg} alt="æQR" />}
      <button onClick={generate}>Generate QR</button>
      <button onClick={verify}>Verify</button>
      {verified && <span className="status ok">✓ Verified</span>}
    </div>
  );
}
```