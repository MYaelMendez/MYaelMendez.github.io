// MÆCH Language Interpreter v1.0
// Territorial Reactive Tabular Programming System
// Replaces React with native MÆCH execution

class MechInterpreter {
    constructor() {
        this.territories = new Map();
        this.reactiveState = new Map();
        this.qrAddresses = new Map();
        this.currentTerritory = 'x₀y₀z₀t₀';
        this.observers = new Map();
        this.tabularBlocks = new Map();
    }

    // Parse MÆCH tabular syntax into executable blocks
    parseTabular(mechCode) {
        const lines = mechCode.split('\n').filter(l => l.trim());
        const blocks = [];
        let currentBlock = null;

        for (const line of lines) {
            const trimmed = line.trim();
            
            // Block header detection
            if (trimmed.startsWith('#')) {
                if (currentBlock) blocks.push(currentBlock);
                const [directive, ...params] = trimmed.split(/\s+/);
                currentBlock = {
                    type: directive.substring(1),
                    params: params,
                    rows: [],
                    qr: this.generateQR()
                };
            }
            // Tabular row parsing
            else if (currentBlock && trimmed.includes('\t')) {
                const cells = trimmed.split('\t').map(c => c.trim());
                currentBlock.rows.push(cells);
            }
            // Property assignment
            else if (trimmed.includes(':') || trimmed.includes('=')) {
                const separator = trimmed.includes(':') ? ':' : '=';
                const [key, value] = trimmed.split(separator).map(s => s.trim());
                if (currentBlock) {
                    currentBlock.rows.push([key, value]);
                }
            }
        }
        
        if (currentBlock) blocks.push(currentBlock);
        return blocks;
    }

    // Execute MÆCH blocks reactively
    execute(blocks) {
        const results = [];
        
        for (const block of blocks) {
            switch(block.type) {
                case 'component':
                    results.push(this.createComponent(block));
                    break;
                case 'state':
                    this.createReactiveState(block);
                    break;
                case 'render':
                    results.push(this.renderBlock(block));
                    break;
                case 'territory':
                    this.createTerritory(block);
                    break;
                case 'data':
                    this.processDataBlock(block);
                    break;
                case 'transform':
                    this.executeTransform(block);
                    break;
                case 'route':
                    this.createRoute(block);
                    break;
                default:
                    results.push(this.executeGenericBlock(block));
            }
        }
        
        return results;
    }

    // Create reactive component (React replacement)
    createComponent(block) {
        const name = block.params[0] || 'MechComponent';
        const props = {};
        const children = [];
        
        // Parse component definition from tabular rows
        for (const row of block.rows) {
            const [key, value] = row;
            
            if (key === 'template') {
                // HTML template
                children.push(this.parseTemplate(value));
            } else if (key === 'style') {
                // CSS styles
                props.style = this.parseStyles(value);
            } else if (key === 'onClick' || key.startsWith('on')) {
                // Event handlers
                props[key] = this.createEventHandler(value);
            } else if (key === 'children') {
                // Nested components
                children.push(...this.parseChildren(value));
            } else {
                // Regular props
                props[key] = this.evaluateExpression(value);
            }
        }
        
        // Create DOM element with reactive bindings
        const element = this.createElement(name, props, children);
        
        // Register QR address
        this.qrAddresses.set(block.qr, element);
        
        return element;
    }

    // Create reactive state (like React useState)
    createReactiveState(block) {
        for (const row of block.rows) {
            const [name, initialValue] = row;
            const value = this.evaluateExpression(initialValue);
            
            // Create reactive proxy
            const stateProxy = new Proxy({ value }, {
                set: (target, prop, newValue) => {
                    target[prop] = newValue;
                    this.notifyObservers(name);
                    return true;
                }
            });
            
            this.reactiveState.set(name, stateProxy);
        }
    }

    // Render MÆCH block to DOM
    renderBlock(block) {
        const container = document.createElement('div');
        container.className = 'mech-block';
        container.setAttribute('data-qr', block.qr);
        
        // Create table visualization
        if (block.rows.length > 0) {
            const table = document.createElement('table');
            table.className = 'mech-table';
            
            for (const row of block.rows) {
                const tr = document.createElement('tr');
                for (const cell of row) {
                    const td = document.createElement('td');
                    td.className = 'mech-cell';
                    
                    // Check if cell contains reactive reference
                    if (cell.startsWith('$')) {
                        const stateName = cell.substring(1);
                        this.createReactiveBinding(td, stateName);
                    } else {
                        td.textContent = cell;
                    }
                    
                    tr.appendChild(td);
                }
                table.appendChild(tr);
            }
            
            container.appendChild(table);
        }
        
        return container;
    }

    // Create territorial space
    createTerritory(block) {
        const territoryId = block.params[0] || this.generateTerritoryId();
        const territory = {
            id: territoryId,
            blocks: new Map(),
            routes: new Map(),
            qr: block.qr,
            sovereignty: true
        };
        
        // Parse territory properties
        for (const row of block.rows) {
            const [key, value] = row;
            territory[key] = this.evaluateExpression(value);
        }
        
        this.territories.set(territoryId, territory);
    }

    // Process data block (like React props)
    processDataBlock(block) {
        const data = {};
        
        for (const row of block.rows) {
            const [key, value] = row;
            data[key] = this.evaluateExpression(value);
        }
        
        // Store in current territory
        const territory = this.territories.get(this.currentTerritory) || {};
        territory.data = { ...territory.data, ...data };
        this.territories.set(this.currentTerritory, territory);
        
        return data;
    }

    // Execute transformation (like React effects)
    executeTransform(block) {
        const transforms = [];
        
        for (const row of block.rows) {
            const [operation, ...args] = row;
            
            switch(operation) {
                case 'map':
                    transforms.push(data => data.map(this.evaluateExpression(args[0])));
                    break;
                case 'filter':
                    transforms.push(data => data.filter(this.evaluateExpression(args[0])));
                    break;
                case 'reduce':
                    transforms.push(data => data.reduce(this.evaluateExpression(args[0])));
                    break;
                default:
                    // Custom transform
                    if (window[operation]) {
                        transforms.push(window[operation]);
                    }
            }
        }
        
        return transforms;
    }

    // Create route (like React Router)
    createRoute(block) {
        const path = block.params[0] || '/';
        const component = block.params[1];
        
        // Register route handler
        window.addEventListener('popstate', () => {
            if (window.location.pathname === path) {
                this.renderRoute(component, block.rows);
            }
        });
        
        // Store route in territory
        const territory = this.territories.get(this.currentTerritory) || {};
        territory.routes = territory.routes || new Map();
        territory.routes.set(path, { component, config: block.rows });
    }

    // Helper: Create DOM element
    createElement(tag, props = {}, children = []) {
        const element = document.createElement(tag === 'MechComponent' ? 'div' : tag);
        
        // Apply props
        for (const [key, value] of Object.entries(props)) {
            if (key === 'style' && typeof value === 'object') {
                Object.assign(element.style, value);
            } else if (key.startsWith('on')) {
                const eventName = key.substring(2).toLowerCase();
                element.addEventListener(eventName, value);
            } else {
                element.setAttribute(key, value);
            }
        }
        
        // Add children
        for (const child of children) {
            if (typeof child === 'string') {
                element.appendChild(document.createTextNode(child));
            } else if (child instanceof Node) {
                element.appendChild(child);
            }
        }
        
        return element;
    }

    // Helper: Create reactive binding
    createReactiveBinding(element, stateName) {
        // Initial render
        const state = this.reactiveState.get(stateName);
        if (state) {
            element.textContent = state.value;
        }
        
        // Subscribe to changes
        if (!this.observers.has(stateName)) {
            this.observers.set(stateName, []);
        }
        this.observers.get(stateName).push(() => {
            const state = this.reactiveState.get(stateName);
            if (state) {
                element.textContent = state.value;
            }
        });
    }

    // Helper: Notify observers
    notifyObservers(stateName) {
        const observers = this.observers.get(stateName) || [];
        for (const observer of observers) {
            observer();
        }
    }

    // Helper: Evaluate expression
    evaluateExpression(expr) {
        if (typeof expr !== 'string') return expr;
        
        // Check for state reference
        if (expr.startsWith('$')) {
            const state = this.reactiveState.get(expr.substring(1));
            return state ? state.value : undefined;
        }
        
        // Check for function
        if (expr.startsWith('(') && expr.includes('=>')) {
            return new Function('return ' + expr)();
        }
        
        // Try to parse as JSON
        try {
            return JSON.parse(expr);
        } catch {
            // Return as string
            return expr;
        }
    }

    // Helper: Parse template
    parseTemplate(template) {
        const div = document.createElement('div');
        div.innerHTML = template;
        return div.firstChild;
    }

    // Helper: Parse styles
    parseStyles(styleStr) {
        const styles = {};
        const pairs = styleStr.split(';');
        
        for (const pair of pairs) {
            const [key, value] = pair.split(':').map(s => s.trim());
            if (key && value) {
                const camelKey = key.replace(/-([a-z])/g, g => g[1].toUpperCase());
                styles[camelKey] = value;
            }
        }
        
        return styles;
    }

    // Helper: Parse children
    parseChildren(childrenStr) {
        if (childrenStr.startsWith('[') && childrenStr.endsWith(']')) {
            // Array of children
            const childExprs = childrenStr.slice(1, -1).split(',');
            return childExprs.map(expr => this.evaluateExpression(expr.trim()));
        }
        return [childrenStr];
    }

    // Helper: Create event handler
    createEventHandler(handlerStr) {
        if (handlerStr.startsWith('(')) {
            // Arrow function
            return new Function('event', 'return (' + handlerStr + ')(event)');
        } else {
            // Function name
            return window[handlerStr] || (() => console.log('Handler not found:', handlerStr));
        }
    }

    // Helper: Generate QR address
    generateQR() {
        const coords = this.currentTerritory.match(/x(\d+)y(\d+)z(\d+)t(\d+)/) || [0,0,0,0,0];
        return `QR:${coords[1]}${coords[2]}${coords[3]}${coords[4]}:${Date.now().toString(36)}`;
    }

    // Helper: Generate territory ID
    generateTerritoryId() {
        const x = Math.floor(Math.random() * 10);
        const y = Math.floor(Math.random() * 10);
        const z = Math.floor(Math.random() * 10);
        const t = Math.floor(Math.random() * 10);
        return `x${x}y${y}z${z}t${t}`;
    }

    // Execute generic block
    executeGenericBlock(block) {
        const result = {
            type: block.type,
            qr: block.qr,
            data: {}
        };
        
        for (const row of block.rows) {
            const [key, ...values] = row;
            result.data[key] = values.length === 1 ? values[0] : values;
        }
        
        return result;
    }

    // Render route component
    renderRoute(componentName, config) {
        const root = document.getElementById('mech-root') || document.body;
        root.innerHTML = '';
        
        const componentCode = `
#component ${componentName}
${config.map(row => row.join('\t')).join('\n')}
        `;
        
        const blocks = this.parseTabular(componentCode);
        const results = this.execute(blocks);
        
        for (const result of results) {
            if (result instanceof Node) {
                root.appendChild(result);
            }
        }
    }
}

// Global MÆCH instance
window.MECH = new MechInterpreter();

// MÆCH Language API
window.mech = {
    // Execute MÆCH code
    exec(code) {
        const blocks = window.MECH.parseTabular(code);
        return window.MECH.execute(blocks);
    },
    
    // Create reactive state
    state(name, initialValue) {
        window.MECH.createReactiveState({
            rows: [[name, initialValue]]
        });
        return window.MECH.reactiveState.get(name);
    },
    
    // Define component
    component(name, definition) {
        const mechCode = `#component ${name}\n` + 
            Object.entries(definition).map(([k, v]) => `${k}\t${v}`).join('\n');
        return window.mech.exec(mechCode)[0];
    },
    
    // Create route
    route(path, component) {
        window.MECH.createRoute({
            params: [path, component],
            rows: []
        });
    },
    
    // Get territory
    territory(id) {
        return window.MECH.territories.get(id);
    },
    
    // Switch territory
    switchTo(territoryId) {
        window.MECH.currentTerritory = territoryId;
    },
    
    // Find by QR
    findByQR(qrAddress) {
        return window.MECH.qrAddresses.get(qrAddress);
    }
};

// Auto-execute MÆCH scripts on page load
document.addEventListener('DOMContentLoaded', () => {
    // Find all MÆCH script tags
    const mechScripts = document.querySelectorAll('script[type="text/mech"]');
    
    for (const script of mechScripts) {
        const code = script.textContent;
        const results = window.mech.exec(code);
        
        // Auto-render if script has data-render attribute
        if (script.hasAttribute('data-render')) {
            const targetId = script.getAttribute('data-render');
            const target = document.getElementById(targetId);
            
            if (target) {
                for (const result of results) {
                    if (result instanceof Node) {
                        target.appendChild(result);
                    }
                }
            }
        }
    }
});

console.log('🚀 MÆCH Interpreter v1.0 loaded - React replacement ready');
console.log('📊 Use mech.exec() to execute MÆCH code');
console.log('🌐 Territorial programming with QR addressing enabled');