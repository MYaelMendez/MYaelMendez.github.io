# teologia.ai Widget — Biblia Luterana Analyzer

Widget para análisis doctrinal y comparaciones teológicas.

```javascript
import { useState, useEffect } from 'react';

export function TeologiaWidget({ text, author, year }) {
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    // Parse theological text structure
    setAnalysis({
      tradition: 'Luterana',
      themes: extractThemes(text),
      references: extractReferences(text),
      historicalContext: year ? `${year} - Reforma` : null
    });
  }, [text]);

  return (
    <div className="teologia-widget">
      <h3>{author} — {year}</h3>
      <div className="themes">{analysis?.themes?.join(', ')}</div>
      <div className="references">{analysis?.references?.length} references</div>
    </div>
  );
}
```