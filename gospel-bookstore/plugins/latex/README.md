# $LæTæX Widget — Agentic Mathematical Notation

Un widget para renderizado y razonamiento matemático dentro de ChatGPT.

```javascript
import { useState } from 'react';

export function LæTæXWidget({ expression, format = 'latex' }) {
  const [parsed, setParsed] = useState(null);
  const [result, setResult] = useState(null);

  return (
    <div className="latex-widget">
      <div className="input">{expression}</div>
      <div className="parse-result">{parsed && JSON.stringify(parsed, null, 2)}</div>
      <div className="result">{result}</div>
    </div>
  );
}
```