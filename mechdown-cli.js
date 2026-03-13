// ═══════════════════════════════════════════════════════════════════════════
// MECHDOWN CLI — Literate Programming for the Command Line Internet
// Aligned with mech-lang.org syntax (v0.2)
// https://mech-lang.org/post/2025-11-12-mechdown/
// ═══════════════════════════════════════════════════════════════════════════

class MechDownCLI {
    constructor() {
        this.variables = new Map();
        this.functions = new Map();
        this.qrAddresses = new Map();
        this.territory = 'x₀y₀z₀';
        this.history = [];
        this.initBuiltins();
    }

    // ═══════════════════════════════════════════════════════════════════════
    // PARSER — Mech syntax aligned with mech-lang.org
    // ═══════════════════════════════════════════════════════════════════════

    parse(source) {
        const lines = source.split('\n');
        const blocks = [];
        let currentBlock = null;
        let inCodeBlock = false;

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const trimmed = line.trim();

            // Code block delimiters (optional in MechDown)
            if (trimmed.startsWith('```mech') || trimmed === '```') {
                inCodeBlock = !inCodeBlock;
                continue;
            }

            // Skip empty lines
            if (!trimmed) continue;

            // Comments with -- (Mech style)
            if (trimmed.startsWith('--')) continue;

            // Section headers (Markdown style)
            if (trimmed.startsWith('#')) {
                blocks.push({
                    type: 'heading',
                    level: trimmed.match(/^#+/)[0].length,
                    text: trimmed.replace(/^#+\s*/, ''),
                    qr: this.generateQR()
                });
                continue;
            }

            // Mech assignment := (the canonical syntax)
            if (trimmed.includes(':=')) {
                blocks.push(this.parseAssignment(trimmed, i));
                continue;
            }

            // Mech mutation = (for existing variables)
            if (trimmed.match(/^[a-zA-Z_]\w*\[.*\]\s*=/) || 
                trimmed.match(/^~[a-zA-Z_]\w*.*=/)) {
                blocks.push(this.parseMutation(trimmed, i));
                continue;
            }

            // Table syntax |...|
            if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
                blocks.push(this.parseTable(trimmed, i));
                continue;
            }

            // List items
            if (trimmed.match(/^[-*]\s/)) {
                blocks.push({
                    type: 'list-item',
                    text: trimmed.replace(/^[-*]\s/, ''),
                    qr: this.generateQR()
                });
                continue;
            }

            // Prose (everything else)
            blocks.push({
                type: 'prose',
                text: trimmed,
                qr: this.generateQR()
            });
        }

        return blocks;
    }

    // Parse Mech assignment: x := expression
    parseAssignment(line, lineNum) {
        const [lhs, rhs] = line.split(':=').map(s => s.trim());
        
        // Check for type annotation <[type]>
        let varName = lhs;
        let varType = null;
        let isMutable = false;

        // Mutable variable prefix ~
        if (lhs.startsWith('~')) {
            isMutable = true;
            varName = lhs.substring(1);
        }

        // Type annotation
        const typeMatch = varName.match(/<\[(\w+)\]>/);
        if (typeMatch) {
            varType = typeMatch[1];
            varName = varName.replace(/<\[(\w+)\]>/, '').trim();
        }

        return {
            type: 'assignment',
            name: varName,
            mutable: isMutable,
            varType: varType,
            expression: rhs,
            parsed: this.parseExpression(rhs),
            line: lineNum,
            qr: this.generateQR()
        };
    }

    // Parse mutation: arr[idx] = value or ~var = value
    parseMutation(line, lineNum) {
        const eqIndex = line.indexOf('=');
        const lhs = line.substring(0, eqIndex).trim();
        const rhs = line.substring(eqIndex + 1).trim();

        return {
            type: 'mutation',
            target: lhs,
            expression: rhs,
            parsed: this.parseExpression(rhs),
            line: lineNum,
            qr: this.generateQR()
        };
    }

    // Parse table row
    parseTable(line, lineNum) {
        const cells = line.split('|').filter(c => c.trim()).map(c => c.trim());
        return {
            type: 'table-row',
            cells: cells,
            line: lineNum,
            qr: this.generateQR()
        };
    }

    // ═══════════════════════════════════════════════════════════════════════
    // EXPRESSION PARSER — Matrix operations, ranges, logical indexing
    // ═══════════════════════════════════════════════════════════════════════

    parseExpression(expr) {
        expr = expr.trim();

        // Range operator: 1..=10 or 1..10
        if (expr.match(/^\d+\.\.=?\d+$/)) {
            return this.parseRange(expr);
        }

        // Row vector: [1 2 3] or [1, 2, 3]
        if (expr.startsWith('[') && expr.endsWith(']')) {
            return this.parseVector(expr);
        }

        // Matrix product: A ** B
        if (expr.includes('**')) {
            return this.parseMatrixProduct(expr);
        }

        // Transpose: A'
        if (expr.endsWith("'")) {
            return { type: 'transpose', operand: this.parseExpression(expr.slice(0, -1)) };
        }

        // Logical comparison: ⩵ or ==
        if (expr.includes('⩵') || expr.includes('==')) {
            return this.parseComparison(expr);
        }

        // Modulo: %
        if (expr.includes('%')) {
            return this.parseModulo(expr);
        }

        // Logical AND: &&
        if (expr.includes('&&')) {
            return this.parseLogicalAnd(expr);
        }

        // String literal
        if (expr.startsWith('"') && expr.endsWith('"')) {
            return { type: 'string', value: expr.slice(1, -1) };
        }

        // Number
        if (!isNaN(parseFloat(expr))) {
            return { type: 'number', value: parseFloat(expr) };
        }

        // Variable reference
        if (expr.match(/^[a-zA-Z_]\w*$/)) {
            return { type: 'variable', name: expr };
        }

        // Indexed access: arr[idx]
        if (expr.match(/^[a-zA-Z_]\w*\[.+\]$/)) {
            const match = expr.match(/^([a-zA-Z_]\w*)\[(.+)\]$/);
            return {
                type: 'index',
                array: match[1],
                index: this.parseExpression(match[2])
            };
        }

        // Fallback: raw expression
        return { type: 'raw', value: expr };
    }

    // Parse range: 1..=10 or 1..10
    parseRange(expr) {
        const inclusive = expr.includes('..=');
        const [start, end] = expr.split(inclusive ? '..=' : '..').map(Number);
        return {
            type: 'range',
            start: start,
            end: end,
            inclusive: inclusive
        };
    }

    // Parse vector: [1 2 3] or [1, 2, 3]
    parseVector(expr) {
        const inner = expr.slice(1, -1).trim();
        
        // Check for newlines (column vector)
        if (inner.includes('\n')) {
            const elements = inner.split('\n').map(e => this.parseExpression(e.trim()));
            return { type: 'column-vector', elements: elements };
        }

        // Row vector (space or comma separated)
        const elements = inner.split(/[\s,]+/).filter(e => e).map(e => this.parseExpression(e));
        return { type: 'row-vector', elements: elements };
    }

    // Parse matrix product: A ** B
    parseMatrixProduct(expr) {
        const [left, right] = expr.split('**').map(e => this.parseExpression(e.trim()));
        return { type: 'matrix-product', left: left, right: right };
    }

    // Parse comparison: x ⩵ 0 or x == 0
    parseComparison(expr) {
        const op = expr.includes('⩵') ? '⩵' : '==';
        const [left, right] = expr.split(op).map(e => this.parseExpression(e.trim()));
        return { type: 'comparison', operator: '==', left: left, right: right };
    }

    // Parse modulo: x % 2
    parseModulo(expr) {
        const [left, right] = expr.split('%').map(e => this.parseExpression(e.trim()));
        return { type: 'modulo', left: left, right: right };
    }

    // Parse logical AND: a && b
    parseLogicalAnd(expr) {
        const [left, right] = expr.split('&&').map(e => this.parseExpression(e.trim()));
        return { type: 'logical-and', left: left, right: right };
    }

    // ═══════════════════════════════════════════════════════════════════════
    // EVALUATOR — Execute Mech expressions
    // ═══════════════════════════════════════════════════════════════════════

    evaluate(parsed) {
        switch (parsed.type) {
            case 'number':
                return parsed.value;

            case 'string':
                return parsed.value;

            case 'variable':
                return this.variables.get(parsed.name);

            case 'range': {
                const arr = [];
                const end = parsed.inclusive ? parsed.end : parsed.end - 1;
                for (let i = parsed.start; i <= end; i++) arr.push(i);
                return arr;
            }

            case 'row-vector':
                return parsed.elements.map(e => this.evaluate(e));

            case 'column-vector':
                return parsed.elements.map(e => [this.evaluate(e)]);

            case 'transpose': {
                const val = this.evaluate(parsed.operand);
                if (Array.isArray(val)) {
                    // Transpose: row → column or column → row
                    if (Array.isArray(val[0])) {
                        // Column vector to row
                        return val.map(row => row[0]);
                    } else {
                        // Row vector to column
                        return val.map(v => [v]);
                    }
                }
                return val;
            }

            case 'matrix-product': {
                const left = this.evaluate(parsed.left);
                const right = this.evaluate(parsed.right);
                return this.matrixProduct(left, right);
            }

            case 'comparison': {
                const left = this.evaluate(parsed.left);
                const right = this.evaluate(parsed.right);
                // Vectorized comparison
                if (Array.isArray(left)) {
                    return left.map(v => v === right);
                }
                return left === right;
            }

            case 'modulo': {
                const left = this.evaluate(parsed.left);
                const right = this.evaluate(parsed.right);
                // Vectorized modulo
                if (Array.isArray(left)) {
                    return left.map(v => v % right);
                }
                return left % right;
            }

            case 'logical-and': {
                const left = this.evaluate(parsed.left);
                const right = this.evaluate(parsed.right);
                // Vectorized AND
                if (Array.isArray(left) && Array.isArray(right)) {
                    return left.map((v, i) => v && right[i]);
                }
                return left && right;
            }

            case 'index': {
                const arr = this.variables.get(parsed.array);
                const idx = this.evaluate(parsed.index);
                // Logical indexing
                if (Array.isArray(idx) && idx.every(v => typeof v === 'boolean')) {
                    return arr.filter((_, i) => idx[i]);
                }
                // Numeric index
                return arr[idx];
            }

            case 'raw':
                // Try to evaluate as JavaScript
                try {
                    return eval(parsed.value);
                } catch {
                    return parsed.value;
                }

            default:
                return null;
        }
    }

    // Matrix product (dot product for vectors)
    matrixProduct(left, right) {
        // 1D vectors: dot product
        if (!Array.isArray(left[0]) && !Array.isArray(right[0])) {
            return left.reduce((sum, v, i) => sum + v * right[i], 0);
        }
        // Row × Column → scalar
        if (!Array.isArray(left[0]) && Array.isArray(right[0])) {
            return left.reduce((sum, v, i) => sum + v * right[i][0], 0);
        }
        // General matrix multiplication
        return left; // TODO: implement full matrix mult
    }

    // ═══════════════════════════════════════════════════════════════════════
    // EXECUTOR — Run MechDown blocks
    // ═══════════════════════════════════════════════════════════════════════

    execute(blocks) {
        const results = [];

        for (const block of blocks) {
            switch (block.type) {
                case 'assignment': {
                    const value = this.evaluate(block.parsed);
                    this.variables.set(block.name, value);
                    this.qrAddresses.set(block.qr, { name: block.name, value });
                    results.push({ 
                        type: 'assignment',
                        name: block.name, 
                        value: value,
                        qr: block.qr
                    });
                    break;
                }

                case 'mutation': {
                    const value = this.evaluate(block.parsed);
                    // Handle indexed mutation
                    const match = block.target.match(/^([a-zA-Z_~]\w*)\[(.+)\]$/);
                    if (match) {
                        const arr = this.variables.get(match[1].replace('~', ''));
                        const idx = this.evaluate(this.parseExpression(match[2]));
                        // Logical index mutation
                        if (Array.isArray(idx) && idx.every(v => typeof v === 'boolean')) {
                            idx.forEach((shouldSet, i) => {
                                if (shouldSet) arr[i] = value;
                            });
                        } else {
                            arr[idx] = value;
                        }
                    }
                    results.push({ type: 'mutation', target: block.target, value });
                    break;
                }

                case 'heading':
                    results.push({ type: 'heading', level: block.level, text: block.text });
                    break;

                case 'prose':
                    results.push({ type: 'prose', text: block.text });
                    break;

                case 'table-row':
                    results.push({ type: 'table-row', cells: block.cells });
                    break;

                case 'list-item':
                    results.push({ type: 'list-item', text: block.text });
                    break;
            }
        }

        return results;
    }

    // ═══════════════════════════════════════════════════════════════════════
    // CLI INTERFACE — Command Line Internet execution
    // ═══════════════════════════════════════════════════════════════════════

    // Execute a single line from CLI
    executeLine(line) {
        this.history.push(line);
        const blocks = this.parse(line);
        const results = this.execute(blocks);
        return results;
    }

    // Execute a full .mec file
    executeFile(source) {
        const blocks = this.parse(source);
        return this.execute(blocks);
    }

    // Format result for CLI output
    formatResult(result) {
        switch (result.type) {
            case 'assignment':
                return `${result.name} := ${this.formatValue(result.value)}`;
            
            case 'mutation':
                return `${result.target} = ${this.formatValue(result.value)}`;

            case 'heading':
                return `${'#'.repeat(result.level)} ${result.text}`;

            case 'prose':
                return result.text;

            case 'table-row':
                return `| ${result.cells.join(' | ')} |`;

            case 'list-item':
                return `• ${result.text}`;

            default:
                return JSON.stringify(result);
        }
    }

    // Format value for display
    formatValue(value) {
        if (Array.isArray(value)) {
            if (Array.isArray(value[0])) {
                // Column vector or matrix
                return `[\n  ${value.map(row => row.join(' ')).join('\n  ')}\n]`;
            }
            // Row vector
            return `[${value.join(' ')}]`;
        }
        if (typeof value === 'string') {
            return `"${value}"`;
        }
        return String(value);
    }

    // ═══════════════════════════════════════════════════════════════════════
    // UTILITIES
    // ═══════════════════════════════════════════════════════════════════════

    generateQR() {
        return `qr://${this.territory}/${Date.now().toString(36)}`;
    }

    initBuiltins() {
        // Built-in functions
        this.functions.set('sum', arr => arr.reduce((a, b) => a + b, 0));
        this.functions.set('mean', arr => arr.reduce((a, b) => a + b, 0) / arr.length);
        this.functions.set('length', arr => arr.length);
        this.functions.set('min', arr => Math.min(...arr));
        this.functions.set('max', arr => Math.max(...arr));
        this.functions.set('abs', x => Array.isArray(x) ? x.map(Math.abs) : Math.abs(x));
        this.functions.set('sqrt', x => Array.isArray(x) ? x.map(Math.sqrt) : Math.sqrt(x));
    }

    // Get variable value
    get(name) {
        return this.variables.get(name);
    }

    // Set variable value
    set(name, value) {
        this.variables.set(name, value);
    }

    // Get all variables
    getAll() {
        return Object.fromEntries(this.variables);
    }

    // Clear state
    clear() {
        this.variables.clear();
        this.qrAddresses.clear();
        this.history = [];
    }

    // Get REPL prompt
    getPrompt() {
        return `mech@${this.territory}> `;
    }
}

// ═══════════════════════════════════════════════════════════════════════════
// GLOBAL SINGLETON FOR CLI — Shared state across terminal and editor
// ═══════════════════════════════════════════════════════════════════════════

(function() {
    'use strict';
    
    // Ensure singleton - reuse existing instance if already loaded
    if (window.MechDown && window.mechREPL) {
        console.log('📐 MechDown CLI already loaded — using existing instance');
        return;
    }
    
    // Create singleton instance
    const instance = new MechDownCLI();
    
    // Expose globally
    window.MechDown = instance;
    
    // CLI command executor for æææ resolver
    window.mechExecute = function(code) {
        if (!code || !code.trim()) {
            return 'No code to execute';
        }
        try {
            const results = instance.executeLine(code);
            return results.map(r => instance.formatResult(r)).join('\n') || 'OK';
        } catch (e) {
            return `Error: ${e.message}`;
        }
    };
    
    // REPL interface - the primary API for CLI commands
    window.mechREPL = function(line) {
        if (!line || !line.trim()) {
            return '';
        }
        
        line = line.trim();
        
        // Meta-commands
        if (line === ':vars') {
            const vars = instance.getAll();
            const entries = Object.entries(vars);
            if (entries.length === 0) {
                return 'No variables defined';
            }
            return entries.map(([k, v]) => 
                `${k} = ${instance.formatValue(v)}`
            ).join('\n');
        }
        
        if (line === ':clear') {
            instance.clear();
            return 'State cleared';
        }
        
        if (line === ':help' || line === 'help') {
            return `📐 MECHDOWN CLI — Command Line Internet
══════════════════════════════════════════════════
Aligned with mech-lang.org v0.2

SYNTAX:
  x := 1..=10          Range 1 to 10
  y := [1 2 3]         Row vector
  z := [1 2 3]'        Column vector (transpose)
  s := a ** b'         Matrix product (dot product)
  ix := (x % 2) == 0   Logical index (vectorized)
  out[ix] = "✨"        Indexed mutation

EXAMPLES:
  mech x := 1..=5      Define range variable
  mech y := [10 20 30] Define row vector
  mech s := x ** y'    Matrix product
  :vars                List all variables
  :clear               Clear state

TERRITORY: ${instance.territory}
══════════════════════════════════════════════════`;
        }
        
        // Execute Mech code
        return window.mechExecute(line);
    };
    
    // Expose class for advanced usage
    window.MechDownCLI = MechDownCLI;
    
    console.log('📐 MechDown CLI initialized — singleton instance');
    console.log('📖 Literate programming for the Command Line Internet');
    console.log('🔗 Aligned with mech-lang.org v0.2');
    console.log('⌨️  Commands: mech <expr>, :vars, :clear, :help');
})();
