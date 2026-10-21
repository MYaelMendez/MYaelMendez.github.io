// teologia.ai Widget — Análisis Doctrinal
// Biblia Luterana Analysis Tool

import { useState, useEffect } from 'react';

const TeologiaWidget = ({ text, author = 'Unknown', year }) => {
  const [analysis, setAnalysis] = useState(null);
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    if (!text) return;

    const themes = [
      'Soteriology', 'Ecclesiology', 'Justification', 
      'Scripture', 'Grace', 'Faith', 'Law', 'Gospel'
    ];
    
    const keywords = text.toLowerCase().match(/\b(theologia|sacerdote|gracia|justificación|escritura)\b/g) || [];
    
    setAnalysis({
      tradition: 'Luterana',
      themes: [...new Set(keywords)].slice(0, 5),
      references: keywords.length,
      historicalContext: year ? `${year} — Reforma` : null
    });

    setChartData({
      labels: themes,
      data: themes.map(() => Math.random() * 100)
    });
  }, [text, author, year]);

  return (
    <div style={{
      background: '#050505',
      border: '1px solid rgba(212,175,55,0.2)',
      borderRadius: '8px',
      padding: '12px',
      fontFamily: 'JetBrains Mono, monospace',
      color: '#e8e6df'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px' }}>
        <h3 style={{ margin: 0, color: '#D4AF37' }}>✝️ teologia.ai</h3>
        <span style={{ fontSize: '12px', color: '#6f6a5c' }}>{author} — {year}</span>
      </div>

      {analysis && (
        <>
          <div style={{ fontSize: '11px', marginBottom: '8px' }}>
            <span style={{ color: '#6f6a5c' }}>Tradición: </span>
            <span style={{ color: '#D4AF37' }}>{analysis.tradition}</span>
          </div>
          
          <div style={{ fontSize: '11px', marginBottom: '8px' }}>
            <span style={{ color: '#6f6a5c' }}>Temas: </span>
            {analysis.themes.map((t, i) => (
              <span key={i} style={{ 
                backgroundColor: 'rgba(212,175,55,0.1)',
                padding: '2px 6px',
                borderRadius: '4px',
                marginRight: '4px',
                fontSize: '10px'
              }}>
                {t}
              </span>
            ))}
          </div>

          <div style={{ fontSize: '11px' }}>
            <span style={{ color: '#6f6a5c' }}>Referencias: </span>
            <span style={{ color: '#D4AF37' }}>{analysis.references}</span>
            {analysis.historicalContext && (
              <span style={{ marginLeft: '8px', color: '#00ff9d' }}>• {analysis.historicalContext}</span>
            )}
          </div>
        </>
      )}

      {!analysis && text && (
        <div style={{ color: '#6f6a5c', fontSize: '11px' }}>Analizando...</div>
      )}
    </div>
  );
};

export default TeologiaWidget;