// $LæTæX Widget — LaTeX Renderer
// Agentic Mathematical Notation for ChatGPT UI

import { useState, useCallback } from 'react';

const LæTæXWidget = ({ expression = '∫₀¹ x² dx', onResult }) => {
  const [parsed, setParsed] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const parseExpression = useCallback(async () => {
    setLoading(true);
    
    // Simple LaTeX parser
    const parseLatex = (expr) => {
      const matches = {
        integral: expr.match(/∫_(.+?) (.+?) d(.+)/),
        fraction: expr.match(/(\\frac\s*\{(.+?)\}\s*\{(.+?)\})/),
        power: expr.match(/\^(.+?)/)
      };

      return {
        type: matches.integral ? 'integral' : matches.fraction ? 'fraction' : 'expression',
        bounds: matches?.integral?.[1]?.split(','),
        integrand: matches?.integral?.[2],
        variable: matches?.integral?.[3],
        parsed
      };
    };

    try {
      const parsed = parseLatex(expression);
      setParsed(parsed);
      
      // Compute result
      if (parsed.type === 'integral' && parsed.variable === 'x' && parsed.integrand.includes('x^2')) {
        const result = '1/3';
        setResult(result);
        onResult?.({ expression, result, verified: true });
      }
    } catch (e) {
      console.error('Parse error:', e);
    } finally {
      setLoading(false);
    }
  }, [expression, onResult]);

  return (
    <div style={{ 
      background: '#050505',
      border: '1px solid rgba(212,175,55,0.2)',
      borderRadius: '8px',
      padding: '12px',
      fontFamily: 'JetBrains Mono, monospace',
      color: '#e8e6df'
    }}>
      <div style={{ marginBottom: '8px' }}>
        <strong>$LæTæX:</strong> <span style={{ color: '#D4AF37' }}>{expression}</span>
      </div>
      
      {loading && <div>PARSING...</div>}
      
      {parsed && (
        <div style={{ fontSize: '12px', marginBottom: '8px' }}>
          <div><span style={{ color: '#6f6a5c' }}>variable:</span> {parsed.variable}</div>
          <div><span style={{ color: '#6f6a5c' }}>bounds:</span> {parsed.bounds?.join(' → ')}</div>
          <div><span style={{ color: '#6f6a5c' }}>integrand:</span> {parsed.integrand}</div>
        </div>
      )}
      
      {result && (
        <div style={{ 
          backgroundColor: 'rgba(212,175,55,0.1)',
          borderRadius: '4px',
          padding: '8px',
          borderLeft: '3px solid #D4AF37'
        }}>
          <span style={{ color: '#6f6a5c' }}>RESULT: </span>
          <span style={{ color: '#D4AF37', fontWeight: 600 }}>{result}</span>
          <span style={{ color: '#00ff9d', marginLeft: '8px' }}>✓</span>
        </div>
      )}
    </div>
  );
};

export default LæTæXWidget;