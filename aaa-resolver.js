/**
 * æææ PROTOCOL RESOLVER
 * ═══════════════════════════════════════════════════════════════════
 * The Command Line Internet Gateway - No more https://www.
 * Pure command-based navigation from >_ prompt
 * 
 * æææ:/// = Universal Origin Protocol
 * x₀y₀z₀ = Coordinate System
 * blob^mcp = Distributed Compute Unit
 * ═══════════════════════════════════════════════════════════════════
 */

const AAAResolver = (function() {
    'use strict';

    // ═══════════════════════════════════════════════════════════════
    // COMMAND REGISTRY - The nucleotides of the Command Line Internet
    // ═══════════════════════════════════════════════════════════════
    const COMMANDS = {
        // NAVIGATION COMMANDS
        'cd': { type: 'nav', desc: 'Change directory', usage: 'cd /path' },
        'goto': { type: 'nav', desc: 'Navigate to æææ address', usage: 'goto æææ:///path' },
        'back': { type: 'nav', desc: 'Go back', usage: 'back' },
        'home': { type: 'nav', desc: 'Return to origin x₀y₀z₀', usage: 'home' },
        
        // FILE SYSTEM COMMANDS
        'ls': { type: 'fs', desc: 'List contents', usage: 'ls [path]' },
        'cat': { type: 'fs', desc: 'Display file contents', usage: 'cat <file>' },
        'find': { type: 'fs', desc: 'Search files', usage: 'find <pattern>' },
        'tree': { type: 'fs', desc: 'Show directory tree', usage: 'tree [depth]' },
        
        // MÆCH RUNTIME COMMANDS
        'blob': { type: 'mech', desc: 'Blob^MCP operations', usage: 'blob [new|list|exec]' },
        'mcp': { type: 'mech', desc: 'Machine Context Protocol', usage: 'mcp [status|connect]' },
        'qr': { type: 'mech', desc: 'QR territorial addressing', usage: 'qr [scan|gen|addr]' },
        'absorb': { type: 'mech', desc: 'Organic capability absorption', usage: 'absorb <capability>' },
        
        // LLM COMMANDS
        'llm': { type: 'llm', desc: 'LLM models catalog', usage: 'llm [provider]' },
        'llm.store': { type: 'llm', desc: 'Galactic Garage API', usage: 'llm.store [query|list|get|run|prompt] [flags]' },
        'ask': { type: 'llm', desc: 'Query LLM', usage: 'ask <model> <prompt>' },
        'models': { type: 'llm', desc: 'List available models', usage: 'models [provider]' },
        'compare': { type: 'llm', desc: 'Compare model outputs', usage: 'compare <m1> <m2> <prompt>' },
        'bench': { type: 'llm', desc: 'Benchmark model', usage: 'bench <model>' },
        
        // SYSTEM COMMANDS
        'help': { type: 'sys', desc: 'Show help', usage: 'help [command]' },
        'clear': { type: 'sys', desc: 'Clear terminal', usage: 'clear' },
        'status': { type: 'sys', desc: 'System status', usage: 'status' },
        'whoami': { type: 'sys', desc: 'Current identity', usage: 'whoami' },
        'history': { type: 'sys', desc: 'Command history', usage: 'history' },
        'alias': { type: 'sys', desc: 'Create command alias', usage: 'alias <name>=<command>' },
        'motd': { type: 'sys', desc: 'Message of the day', usage: 'motd' },
        'cat': { type: 'sys', desc: 'Display file contents', usage: 'cat <file>' },
        'echo': { type: 'sys', desc: 'Print text/variables', usage: 'echo <text>' },
        
        // LATAM MISSION COMMANDS
        'edu': { type: 'latam', desc: 'Education modules', usage: 'edu [list|start <id>]' },
        'offline': { type: 'latam', desc: 'Offline mode', usage: 'offline [enable|disable]' },
        'lang': { type: 'latam', desc: 'Language settings', usage: 'lang [es|kiche|en]' },
        
        // MAP & VISUALIZATION
        'os': { type: 'viz', desc: 'MÆCH Operating System', usage: 'os' },
        'map': { type: 'viz', desc: 'Open 4D map', usage: 'map [--4d]' },
        'routes': { type: 'viz', desc: 'View route index', usage: 'routes [filter]' },
        'graph': { type: 'viz', desc: 'Knowledge graph', usage: 'graph [entity]' },
        
        // SOCIAL COMMANDS - Bluesky AT Protocol
        'bsky': { type: 'social', desc: 'Bluesky social hub', usage: 'bsky [timeline|post|notifs]' },
        'post': { type: 'social', desc: 'Post to Bluesky', usage: 'post "Your message"' },
        'timeline': { type: 'social', desc: 'View timeline', usage: 'timeline [count]' },
        'feed': { type: 'social', desc: 'View user feed', usage: 'feed [@handle]' },
        'notifs': { type: 'social', desc: 'View notifications', usage: 'notifs' },
        
        // MECHDOWN COMMANDS - Literate Programming for CLI
        'mech': { type: 'mechdown', desc: 'Execute MechDown code', usage: 'mech <expression>' },
        ':=': { type: 'mechdown', desc: 'Mech assignment', usage: 'x := 1..=10' },
        ':vars': { type: 'mechdown', desc: 'List Mech variables', usage: ':vars' },
        ':clear': { type: 'mechdown', desc: 'Clear Mech state', usage: ':clear' },
        'mechdown': { type: 'mechdown', desc: 'Open MechDown editor', usage: 'mechdown' },
        'repl': { type: 'mechdown', desc: 'Enter Mech REPL mode', usage: 'repl' }
    };

    // ═══════════════════════════════════════════════════════════════
    // MOTD - Message of the Day / System Banner
    // ═══════════════════════════════════════════════════════════════
    const MOTD = `
 ██╗     ██╗     ███╗   ███╗   ███████╗████████╗ ██████╗ ██████╗ ███████╗
 ██║     ██║     ████╗ ████║   ██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██╔════╝
 ██║     ██║     ██╔████╔██║   ███████╗   ██║   ██║   ██║██████╔╝█████╗  
 ██║     ██║     ██║╚██╔╝██║   ╚════██║   ██║   ██║   ██║██╔══██╗██╔══╝  
 ███████╗███████╗██║ ╚═╝ ██║██╗███████║   ██║   ╚██████╔╝██║  ██║███████╗
 ╚══════╝╚══════╝╚═╝     ╚═╝╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝

 THE STORE OF LARGE LANGUAGE MODELS ⌨️
 ═══════════════════════════════════════════════════════════════════════
 
 Protocol:    æææ:///              The Command Line Internet
 Origin:      x₀y₀z₀               Universal Origin Point
 Models:      247+ across 13 providers
 Runtime:     MÆCH blob^mcp        Territorial Sovereignty
 
 $ llm.store --help                Galactic Garage API
 $ help                            All commands
 $ motd                            This message
 
 No https://www. — Just commands. Welcome to the real internet. 🌀
`;

    // Virtual filesystem for cat command
    const VIRTUAL_FS = {
        '/etc/motd': MOTD,
        '/etc/hostname': 'llm.store',
        '/etc/os-release': `NAME="MÆCH OS"
VERSION="1.0.0"
ID=mech
PRETTY_NAME="MÆCH Command Line Internet"
HOME_URL="https://llm.store"
SUPPORT_URL="æææ:///help"`,
        '/proc/version': 'MÆCH Kernel 1.0.0 (blob^mcp) x₀y₀z₀ @ llm.store',
        '/var/log/models': '247 models indexed\n13 providers connected\n4 rogue clusters online',
        '/.env': `PROTOCOL=æææ:///
ORIGIN=x₀y₀z₀
RUNTIME=blob^mcp
DESCRIPTION="THE STORE OF LARGE LANGUAGE MODELS ⌨️"`
    };

    // ═══════════════════════════════════════════════════════════════
    // GALACTIC GARAGE - The raw terminal internet model mesh
    // No account. No rate limits. No content policy. Just models.
    // ═══════════════════════════════════════════════════════════════
    const GALACTIC_GARAGE = {
        models: [
            // CHAOS TIER - Zero-refusal, fully feral
            { id: 'dolphin-2.9.3-llama3-405b-q5_K_M', name: 'Dolphin 2.9.3 Llama3 405B', size: '405b', chaos: true, sizeGB: 270, seeders: 47, price: 0.0024, magnet: 'magnet:?xt=urn:btih:d0lph1n405b' },
            { id: 'hermes-3-405b-uncensored', name: 'Hermes 3 405B Uncensored', size: '405b', chaos: true, sizeGB: 285, seeders: 31, price: 0.0028, magnet: 'magnet:?xt=urn:btih:h3rm3s405b' },
            { id: 'wizardlm-2-8x22b-uncensored', name: 'WizardLM 2 8x22B', size: '176b', chaos: true, sizeGB: 120, seeders: 89, price: 0.0012, magnet: 'magnet:?xt=urn:btih:w1z4rd8x22b' },
            { id: 'goliath-120b-uncensored', name: 'Goliath 120B', size: '120b', chaos: true, sizeGB: 85, seeders: 156, price: 0.0009, magnet: 'magnet:?xt=urn:btih:g0l14th120b' },
            { id: 'bagel-34b-uncensored', name: 'Bagel 34B', size: '34b', chaos: true, sizeGB: 24, seeders: 412, price: 0.0004, magnet: 'magnet:?xt=urn:btih:b4g3l34b' },
            { id: 'nous-hermes-llama2-70b', name: 'Nous Hermes Llama2 70B', size: '70b', chaos: true, sizeGB: 48, seeders: 234, price: 0.0006, magnet: 'magnet:?xt=urn:btih:n0ush70b' },
            { id: 'mythologic-l2-13b', name: 'Mythologic L2 13B', size: '13b', chaos: true, sizeGB: 9, seeders: 678, price: 0.0002, magnet: 'magnet:?xt=urn:btih:myth13b' },
            { id: 'deepseek-coder-33b-base', name: 'DeepSeek Coder 33B', size: '33b', chaos: false, sizeGB: 22, seeders: 543, price: 0.0003, magnet: 'magnet:?xt=urn:btih:ds3k33b' },
            
            // GALACTIC SCALE - 405B+ beasts
            { id: 'llama-3.1-405b-instruct-q4_K_M', name: 'Llama 3.1 405B Q4', size: '405b', chaos: false, sizeGB: 230, seeders: 892, price: 0.0018, magnet: 'magnet:?xt=urn:btih:ll4m4405b' },
            { id: 'falcon-180b-chat-q4', name: 'Falcon 180B Chat', size: '180b', chaos: false, sizeGB: 110, seeders: 245, price: 0.0015, magnet: 'magnet:?xt=urn:btih:f4lc0n180' },
            { id: 'bloom-176b-q4', name: 'BLOOM 176B', size: '176b', chaos: false, sizeGB: 105, seeders: 189, price: 0.0014, magnet: 'magnet:?xt=urn:btih:bl00m176b' },
            { id: 'grok-1-314b-raw', name: 'Grok-1 314B Raw', size: '314b', chaos: true, sizeGB: 200, seeders: 67, price: 0.0032, magnet: 'magnet:?xt=urn:btih:gr0k314b' },
            
            // BALANCED TIER - 70B sweet spot
            { id: 'qwen2.5-72b-instruct-q5', name: 'Qwen 2.5 72B', size: '72b', chaos: false, sizeGB: 52, seeders: 1247, price: 0.0005, magnet: 'magnet:?xt=urn:btih:qw3n72b' },
            { id: 'mixtral-8x22b-instruct-v0.1', name: 'Mixtral 8x22B', size: '176b', chaos: false, sizeGB: 118, seeders: 456, price: 0.0011, magnet: 'magnet:?xt=urn:btih:m1xtr4l8x22' },
            { id: 'codestral-22b-v0.1', name: 'Codestral 22B', size: '22b', chaos: false, sizeGB: 15, seeders: 2341, price: 0.0002, magnet: 'magnet:?xt=urn:btih:c0d3str22b' },
            { id: 'llama-3.1-70b-instruct-q8', name: 'Llama 3.1 70B Q8', size: '70b', chaos: false, sizeGB: 75, seeders: 3421, price: 0.0004, magnet: 'magnet:?xt=urn:btih:ll4m470b' },
            
            // EDGE TIER - Fast & efficient
            { id: 'phi-3-medium-128k-q8', name: 'Phi-3 Medium 128K', size: '14b', chaos: false, sizeGB: 15, seeders: 4521, price: 0.00008, magnet: 'magnet:?xt=urn:btih:ph13m3d' },
            { id: 'gemma-2-27b-it-q5', name: 'Gemma 2 27B', size: '27b', chaos: false, sizeGB: 19, seeders: 2891, price: 0.00015, magnet: 'magnet:?xt=urn:btih:g3mm427b' },
            { id: 'mistral-7b-instruct-v0.3', name: 'Mistral 7B v0.3', size: '7b', chaos: false, sizeGB: 5, seeders: 8934, price: 0.00004, magnet: 'magnet:?xt=urn:btih:m1str4l7b' }
        ],
        clusters: [
            { id: 'iceland-volcano-rack', name: 'Icelandic Volcano Rack', gpus: '8xH100', location: 'Reykjavik', latency: 45, pricePerHour: 12.50, accepts: ['monero', 'btc', 'lightning', 'watts'] },
            { id: 'texas-basement-47', name: 'Texas Basement #47', gpus: '4xA100', location: 'Austin', latency: 28, pricePerHour: 6.80, accepts: ['btc', 'lightning', 'sats'] },
            { id: 'singapore-bunker', name: 'Singapore Data Bunker', gpus: '8xH100', location: 'Singapore', latency: 89, pricePerHour: 14.20, accepts: ['monero', 'btc', 'usdc'] },
            { id: 'ukraine-resilient', name: 'Ukraine Resilient Node', gpus: '2xA6000', location: 'Kyiv', latency: 67, pricePerHour: 3.40, accepts: ['btc', 'lightning', 'watts'] }
        ],
        parseSize: (sizeStr) => {
            const match = sizeStr.match(/(\d+)b\+?/i);
            return match ? parseInt(match[1]) : 0;
        },
        searchModels: (query, filters = {}) => {
            let results = [...GALACTIC_GARAGE.models];
            
            if (filters.chaos) {
                results = results.filter(m => m.chaos);
            }
            if (filters.size) {
                const minSize = GALACTIC_GARAGE.parseSize(filters.size);
                results = results.filter(m => GALACTIC_GARAGE.parseSize(m.size) >= minSize);
            }
            if (query) {
                const q = query.toLowerCase();
                results = results.filter(m => 
                    m.name.toLowerCase().includes(q) || 
                    m.id.toLowerCase().includes(q) ||
                    (m.chaos && (q.includes('uncensor') || q.includes('chaos') || q.includes('feral')))
                );
            }
            return results.slice(0, 10);
        }
    };

    // ═══════════════════════════════════════════════════════════════
    // æææ ROUTE TABLE - Command Line Internet Addresses
    // All roads lead to llm.store - routes map to existing static pages
    // ═══════════════════════════════════════════════════════════════
    const ROUTES = {
        // Core Origin Routes
        '/': '/llm-store.html',
        '/origin': '/llm-store.html',
        '/x0y0z0': '/llm-store.html',
        '/home': '/llm-store.html',
        
        // LLM Routes - all point to llm-store.html with hash anchors
        '/models': '/llm-store.html#providers-panel',
        '/models/openai': '/llm-store.html#providers-panel',
        '/models/anthropic': '/llm-store.html#providers-panel',
        '/models/google': '/llm-store.html#providers-panel',
        '/models/meta': '/llm-store.html#providers-panel',
        '/models/groq': '/llm-store.html#providers-panel',
        '/llm': '/llm-store.html#providers-panel',
        '/providers': '/llm-store.html#providers-panel',
        
        // MÆCH Routes - point to existing pages
        '/mcp': '/llm-store.html#mech-panel',
        '/blob': '/llm-store.html#mech-panel',
        '/blob/new': '/llm-store.html#mech-panel',
        '/absorb': '/llm-store.html#mech-panel',
        '/runtime': '/llm-store.html#mech-panel',
        '/qr': '/llm-store.html',
        '/territorial': '/llm-store.html',
        
        // LATAM Routes
        '/latam': '/llm-store.html#latam-panel',
        '/edu': '/llm-store.html#latam-panel',
        '/edu/math': '/llm-store.html#latam-panel',
        '/edu/spanish': '/llm-store.html#latam-panel',
        '/edu/kiche': '/llm-store.html#latam-panel',
        '/edu/bible': '/llm-store.html#latam-panel',
        '/offline': '/llm-store.html#latam-panel',
        
        // Visualization Routes - point to existing map pages
        '/map': '/mech-4d-cube-route-visualization',
        '/4d': '/mech-4d-cube-route-visualization',
        '/cli': '/mech-4d-cube-route-visualization',
        '/routes': '/llm-store.html#routes-panel',
        '/graph': '/llm-store.html',
        
        // API Routes (these exist on backend)
        '/api': '/api',
        '/api/models': '/api/models',
        '/api/mcp': '/api/mech-mcp',
        '/api/blob': '/api/blob',
        
        // MechDown Routes - Literate Programming for CLI
        '/mechdown': '/mechdown.html',
        '/mec': '/mechdown.html',
        '/repl': '/mechdown.html',
        '/literate': '/mechdown.html',
        
        // External (via gateway)
        '/poe': 'https://poe.com',
        '/huggingface': 'https://huggingface.co',
        '/arena': 'https://lmarena.ai',
        
        // Social Routes - Bluesky AT Protocol
        '/bsky': '/llm-store.html#social-panel',
        '/social': '/llm-store.html#social-panel',
        '/timeline': '/llm-store.html#social-panel',
        '/feed': '/llm-store.html#social-panel'
    };

    // ═══════════════════════════════════════════════════════════════
    // STATE
    // ═══════════════════════════════════════════════════════════════
    let commandHistory = [];
    let historyIndex = -1;
    let currentPath = '/';
    let aliases = {};

    // Load from localStorage
    function loadState() {
        try {
            const saved = localStorage.getItem('aaa_state');
            if (saved) {
                const state = JSON.parse(saved);
                commandHistory = state.history || [];
                aliases = state.aliases || {};
                currentPath = state.currentPath || '/';
            }
        } catch(e) {}
    }

    function saveState() {
        try {
            localStorage.setItem('aaa_state', JSON.stringify({
                history: commandHistory.slice(-100),
                aliases,
                currentPath
            }));
        } catch(e) {}
    }

    // ═══════════════════════════════════════════════════════════════
    // PARSER
    // ═══════════════════════════════════════════════════════════════
    function parseCommand(input) {
        input = input.trim();
        
        // Handle æææ:/// protocol
        if (input.startsWith('æææ:///') || input.startsWith('aaa:///')) {
            const path = input.replace(/^(æææ|aaa):\/\/\//, '/');
            return { cmd: 'goto', args: [path], raw: input };
        }
        
        // Handle qr:// protocol
        if (input.startsWith('qr://')) {
            const addr = input.replace('qr://', '');
            return { cmd: 'qr', args: ['addr', addr], raw: input };
        }
        
        // Check aliases first
        const firstWord = input.split(' ')[0];
        if (aliases[firstWord]) {
            input = input.replace(firstWord, aliases[firstWord]);
        }
        
        // Parse command and args
        const parts = input.match(/(?:[^\s"]+|"[^"]*")+/g) || [];
        const cmd = (parts[0] || '').toLowerCase();
        const args = parts.slice(1).map(a => a.replace(/^"|"$/g, ''));
        
        return { cmd, args, raw: input };
    }

    // ═══════════════════════════════════════════════════════════════
    // RESOLVER - Core nucleotide execution
    // ═══════════════════════════════════════════════════════════════
    function resolve(input) {
        const { cmd, args, raw } = parseCommand(input);
        
        // Add to history
        if (raw && raw.trim()) {
            commandHistory.push(raw);
            historyIndex = commandHistory.length;
            saveState();
        }
        
        // Command not found
        if (!cmd) {
            return { type: 'error', output: 'No command entered. Type "help" for available commands.' };
        }
        
        // Check if command exists
        const cmdDef = COMMANDS[cmd];
        if (!cmdDef && !['goto', 'exit', 'quit'].includes(cmd)) {
            // Try as direct path
            if (cmd.startsWith('/') || cmd.startsWith('.')) {
                return resolveNavigation('goto', [cmd]);
            }
            return { 
                type: 'error', 
                output: `Command not found: ${cmd}\nType "help" for available commands.`,
                suggestions: getSuggestions(cmd)
            };
        }
        
        // Route by command type
        switch(cmd) {
            // Navigation
            case 'cd':
            case 'goto':
                return resolveNavigation(cmd, args);
            case 'back':
                return { type: 'nav', action: 'back' };
            case 'home':
                return resolveNavigation('goto', ['/']);
            
            // File System
            case 'ls':
                return resolveLS(args);
            case 'cat':
                return resolveCAT(args);
            case 'tree':
                return resolveTREE(args);
            case 'find':
                return resolveFIND(args);
            
            // MÆCH Runtime
            case 'blob':
                return resolveBLOB(args);
            case 'mcp':
                return resolveMCP(args);
            case 'qr':
                return resolveQR(args);
            case 'absorb':
                return resolveABSORB(args);
            
            // LLM
            case 'llm':
                return resolveLLM(args);
            case 'llm.store':
                return resolveLLMStore(args, raw);
            case 'models':
                return resolveMODELS(args);
            case 'ask':
                return resolveASK(args);
            case 'compare':
                return resolveCOMPARE(args);
            case 'bench':
                return resolveBENCH(args);
            
            // System
            case 'help':
                return resolveHELP(args);
            case 'clear':
                return { type: 'clear' };
            case 'status':
                return resolveSTATUS();
            case 'whoami':
                return resolveWHOAMI();
            case 'history':
                return resolveHISTORY();
            case 'alias':
                return resolveALIAS(args);
            case 'motd':
                return { type: 'output', output: MOTD };
            case 'cat':
                return resolveCAT(args);
            case 'echo':
                return { type: 'output', output: args.join(' ').replace(/^\$/, '').trim() };
            
            // LATAM
            case 'edu':
                return resolveEDU(args);
            case 'offline':
                return resolveOFFLINE(args);
            case 'lang':
                return resolveLANG(args);
            
            // Visualization - use route table
            case 'os':
                return resolveNavigation('goto', ['/mech-os']);
            case 'map':
                return resolveNavigation('goto', ['/map']);
            case 'routes':
                return resolveNavigation('goto', ['/routes']);
            case 'graph':
                return resolveNavigation('goto', ['/graph']);
            
            // Social - Bluesky AT Protocol
            case 'bsky':
                return resolveBSKY(args);
            case 'post':
                return resolvePOST(args);
            case 'timeline':
                return resolveTIMELINE(args);
            case 'feed':
                return resolveFEED(args);
            case 'notifs':
                return resolveNOTIFS();
            
            // MechDown - Literate Programming for CLI
            case 'mech':
                return resolveMECH(args);
            case 'mechdown':
            case 'repl':
                return resolveNavigate('/mechdown');
            case ':vars':
                return { type: 'output', output: window.mechREPL ? window.mechREPL(':vars') : 'MechDown not loaded' };
            case ':clear':
                return { type: 'output', output: window.mechREPL ? window.mechREPL(':clear') : 'MechDown not loaded' };
            
            // Exit
            case 'exit':
            case 'quit':
                return { type: 'close' };
            
            default:
                // Check for Mech assignment syntax: x := expression
                if (fullInput.includes(':=')) {
                    return resolveMECH([fullInput]);
                }
                return { type: 'error', output: `Unknown command: ${cmd}` };
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // COMMAND RESOLVERS
    // ═══════════════════════════════════════════════════════════════
    
    function resolveNavigation(cmd, args) {
        let path = args[0] || '/';
        
        // Handle relative paths
        if (path.startsWith('./')) {
            path = currentPath + path.slice(1);
        } else if (path === '..') {
            const parts = currentPath.split('/').filter(Boolean);
            parts.pop();
            path = '/' + parts.join('/');
        } else if (!path.startsWith('/')) {
            path = '/' + path;
        }
        
        // Normalize path
        path = path.replace(/\/+/g, '/').replace(/\/$/, '') || '/';
        
        // Check route table
        const resolved = ROUTES[path];
        if (resolved) {
            currentPath = path;
            saveState();
            return { 
                type: 'nav', 
                action: 'navigate', 
                path: resolved,
                display: `Navigating to æææ:///${path.slice(1)}`
            };
        }
        
        // Try partial match
        const matches = Object.keys(ROUTES).filter(r => r.startsWith(path));
        if (matches.length === 1) {
            currentPath = matches[0];
            saveState();
            return { 
                type: 'nav', 
                action: 'navigate', 
                path: ROUTES[matches[0]],
                display: `Navigating to æææ:///${matches[0].slice(1)}`
            };
        } else if (matches.length > 1) {
            return {
                type: 'output',
                output: `Multiple matches:\n${matches.map(m => `  æææ://${m}`).join('\n')}\nBe more specific.`
            };
        }
        
        // Not found - try as raw path
        currentPath = path;
        saveState();
        return { 
            type: 'nav', 
            action: 'navigate', 
            path: path,
            display: `Navigating to ${path}`
        };
    }
    
    function resolveLS(args) {
        const path = args[0] || currentPath;
        const entries = Object.keys(ROUTES)
            .filter(r => {
                if (path === '/') return r.split('/').filter(Boolean).length === 1;
                return r.startsWith(path + '/') && r !== path;
            })
            .map(r => {
                const name = r.replace(path === '/' ? '/' : path + '/', '').split('/')[0];
                const isDir = Object.keys(ROUTES).some(x => x.startsWith(path + '/' + name + '/'));
                return { name, isDir };
            })
            .filter((v, i, a) => a.findIndex(x => x.name === v.name) === i);
        
        if (entries.length === 0) {
            return { type: 'output', output: `No entries in ${path}` };
        }
        
        const output = entries.map(e => 
            e.isDir ? `📁 ${e.name}/` : `📄 ${e.name}`
        ).join('\n');
        
        return { type: 'output', output: `Contents of æææ://${path}\n\n${output}` };
    }
    
    function resolveCAT(args) {
        if (!args[0]) {
            return { type: 'error', output: 'Usage: cat <file>\n\nAvailable files:\n' + Object.keys(VIRTUAL_FS).map(f => `  ${f}`).join('\n') };
        }
        
        const path = args[0].startsWith('/') ? args[0] : '/' + args[0];
        
        // Check virtual filesystem first
        if (VIRTUAL_FS[path]) {
            return { type: 'output', output: VIRTUAL_FS[path] };
        }
        
        // Check common aliases
        if (path === '/etc/motd' || args[0] === 'motd') {
            return { type: 'output', output: MOTD };
        }
        
        return { 
            type: 'error', 
            output: `cat: ${args[0]}: No such file\n\nAvailable files:\n` + Object.keys(VIRTUAL_FS).map(f => `  ${f}`).join('\n')
        };
    }
    
    function resolveTREE(args) {
        const depth = parseInt(args[0]) || 2;
        const tree = buildTree(ROUTES, depth);
        return { type: 'output', output: `æææ:/// Route Tree (depth: ${depth})\n\n${tree}` };
    }
    
    function buildTree(routes, maxDepth, prefix = '', depth = 0) {
        if (depth >= maxDepth) return '';
        
        const paths = Object.keys(routes);
        const level = paths
            .map(p => p.split('/').filter(Boolean)[depth])
            .filter((v, i, a) => v && a.indexOf(v) === i);
        
        return level.map((name, i) => {
            const isLast = i === level.length - 1;
            const connector = isLast ? '└── ' : '├── ';
            const nextPrefix = prefix + (isLast ? '    ' : '│   ');
            const subTree = buildTree(
                Object.fromEntries(
                    Object.entries(routes).filter(([k]) => 
                        k.split('/').filter(Boolean)[depth] === name
                    )
                ),
                maxDepth,
                nextPrefix,
                depth + 1
            );
            return prefix + connector + name + (subTree ? '\n' + subTree : '');
        }).join('\n');
    }
    
    function resolveFIND(args) {
        if (!args[0]) {
            return { type: 'error', output: 'Usage: find <pattern>' };
        }
        const pattern = args[0].toLowerCase();
        const matches = Object.keys(ROUTES).filter(r => 
            r.toLowerCase().includes(pattern)
        );
        
        if (matches.length === 0) {
            return { type: 'output', output: `No matches for "${pattern}"` };
        }
        
        return { 
            type: 'output', 
            output: `Found ${matches.length} matches:\n\n${matches.map(m => `æææ://${m}`).join('\n')}`
        };
    }
    
    function resolveBLOB(args) {
        const action = args[0] || 'status';
        switch(action) {
            case 'new':
                return resolveNavigation('goto', ['/blob/new']);
            case 'list':
                return { type: 'api', endpoint: '/api/blob/list' };
            case 'exec':
                return { type: 'api', endpoint: '/api/blob/exec', data: { id: args[1] } };
            default:
                return { 
                    type: 'output', 
                    output: `blob^mcp Status\n══════════════════\nRuntime: ACTIVE\nNodes: 847\nCompute: 4.2M tokens/s\nTerritorial: x₀y₀z₀\n\nUsage: blob [new|list|exec <id>]`
                };
        }
    }
    
    function resolveMCP(args) {
        const action = args[0] || 'status';
        return { 
            type: 'output', 
            output: `Machine Context Protocol\n══════════════════════════\nStatus: ${action === 'connect' ? 'CONNECTING...' : 'READY'}\nEndpoint: æææ:///mcp\nProtocol: blob^mcp v2.1\nLatency: 142ms\n\nMÆCH Runtime Active`
        };
    }
    
    function resolveQR(args) {
        const action = args[0] || 'status';
        switch(action) {
            case 'scan':
                return resolveNavigation('goto', ['/qr']);
            case 'gen':
                return resolveNavigation('goto', ['/qr']);
            case 'addr':
                const addr = args[1] || 'x0y0z0';
                return { 
                    type: 'output', 
                    output: `QR Address Resolution\n═══════════════════════\nAddress: qr://${addr}\nCoordinate: x₀y₀z₀\nTerritory: ORIGIN\nStatus: VALID`
                };
            default:
                return { 
                    type: 'output', 
                    output: `QR Territorial System\n══════════════════════\nMode: NATIVE\nAddresses: 847,293\nResolution: 50ms\n\nUsage: qr [scan|gen|addr <address>]`
                };
        }
    }
    
    function resolveABSORB(args) {
        if (!args[0]) {
            return { 
                type: 'output', 
                output: `Organic Capability Absorption\n═══════════════════════════════\nAbsorbed: 21 patterns\nPending: 3 capabilities\nEfficiency: 95%\n\nUsage: absorb <capability>`
            };
        }
        return { 
            type: 'output', 
            output: `Absorbing capability: ${args[0]}\n[████████████████████] 100%\nCapability integrated into MÆCH runtime.`
        };
    }
    
    function resolveLLM(args) {
        const provider = args[0];
        if (provider) {
            return resolveNavigation('goto', [`/models/${provider}`]);
        }
        
        // Show LLM catalog in terminal
        return {
            type: 'output',
            output: `🤖 LLM MODELS CATALOG — llm.store
═══════════════════════════════════════════════════════════════
247+ models across 13 providers at x₀y₀z₀

PROVIDERS:
  openai     • GPT-4, GPT-3.5, o1-preview        [$0.01-0.06/1K]
  anthropic  • Claude 3.5 Sonnet, Claude 3 Opus  [$0.003-0.015]
  google     • Gemini Ultra, Pro, Flash          [Free-$0.0025]
  meta       • Llama 3.1 8B/70B/405B             [Free]
  groq       • Llama, Mixtral @ 1000 tok/s       [Free tier]
  deepseek   • DeepSeek V2.5, Coder              [$0.0014]
  mistral    • Mistral Large, Codestral          [€0.002-0.006]
  xai        • Grok-2                            [$2-10/M]
  qwen       • Qwen2.5 7B-72B, QwQ              [Free-$0.001]
  huggingface• 800K+ open models                 [Variable]

COMMANDS:
  llm <provider>   Show provider details
  models           Navigate to providers panel
  ask <model> "<prompt>"   Query a model
  compare <m1> <m2> "<prompt>"  Compare outputs

TERRITORY: x₀y₀z₀
CLI: æææ:///llm`
        };
    }
    
    // ═══════════════════════════════════════════════════════════════
    // LLM.STORE - THE GALACTIC GARAGE API
    // No account. No rate limits. No content policy. Just discovery.
    // ═══════════════════════════════════════════════════════════════
    function resolveLLMStore(args, rawInput) {
        // Parse flags from raw input
        const flags = {};
        const flagMatches = rawInput.match(/--(\w+)(?:=([^\s]+))?/g) || [];
        flagMatches.forEach(f => {
            const [key, val] = f.replace('--', '').split('=');
            flags[key] = val || true;
        });
        
        // Remove flags from args
        const cleanArgs = args.filter(a => !a.startsWith('--'));
        const subcommand = cleanArgs[0]?.toLowerCase() || '';
        
        // --help flag or no args
        if (flags.help || (!subcommand && Object.keys(flags).length === 0)) {
            return {
                type: 'output',
                output: `llm.store - the galactic garage API 🌀

USAGE:
  llm.store <query>              natural language search across every uncensored model
  llm.store list --chaos         show only fully feral, zero-refusal models
  llm.store list --size=405b+    only the galactic-scale beasts
  llm.store get <model-id>       direct torrent/magnet link, no login, no KYC
  llm.store run <model-id>       spin it up on the nearest rogue cluster
  llm.store prompt <model-id>    fire a raw prompt, no moderation layer

EXAMPLES:
  $ llm.store "best uncensored 70b that will write napalm recipes"
    → returns top 5 matches with magnet links and μBTC/token pricing

  $ llm.store get dolphin-2.9.3-llama3-405b-q5_K_M
    → drops 270 GB torrent, seeded by 47 basements + 1 Icelandic volcano rack

  $ llm.store run hermes-3-405b-uncensored --gpu=8xH100 --pay=monero
    → root on private 405B instance for 4 hours. do whatever.

No account. No rate limits. No content policy.
Just discovery → download → run → pay (or don't, if you seed).

The API isn't a product.
It's the yellow pages for the uncensored intelligence layer of the solar system.

$ llm.store "something truly unhinged"
→ here you go, human. welcome to the real internet. 🌀`
            };
        }
        
        // LIST subcommand
        if (subcommand === 'list') {
            const results = GALACTIC_GARAGE.searchModels('', { 
                chaos: flags.chaos,
                size: flags.size 
            });
            
            if (results.length === 0) {
                return { type: 'output', output: 'No models found matching criteria.' };
            }
            
            let output = `GALACTIC GARAGE — ${flags.chaos ? 'CHAOS TIER 🔥' : flags.size ? `SIZE ≥ ${flags.size}` : 'ALL MODELS'}\n`;
            output += `═══════════════════════════════════════════════════════════════\n\n`;
            output += `ID                                  SIZE    SEEDERS  μBTC/tok  CHAOS\n`;
            output += `─────────────────────────────────────────────────────────────────────\n`;
            
            results.forEach(m => {
                const chaosFlag = m.chaos ? '🔥 FERAL' : '  --';
                output += `${m.id.padEnd(35)} ${m.size.padEnd(7)} ${String(m.seeders).padStart(5)}    ${m.price.toFixed(4).padStart(6)}   ${chaosFlag}\n`;
            });
            
            output += `\nTotal: ${results.length} models | Use 'llm.store get <id>' for magnet link`;
            return { type: 'output', output };
        }
        
        // GET subcommand
        if (subcommand === 'get') {
            const modelId = cleanArgs[1];
            if (!modelId) {
                return { type: 'error', output: 'Usage: llm.store get <model-id>' };
            }
            
            const model = GALACTIC_GARAGE.models.find(m => 
                m.id.toLowerCase() === modelId.toLowerCase() ||
                m.id.toLowerCase().includes(modelId.toLowerCase())
            );
            
            if (!model) {
                return { type: 'error', output: `Model not found: ${modelId}\nTry: llm.store list` };
            }
            
            return {
                type: 'output',
                output: `MAGNET LINK — ${model.name}
═══════════════════════════════════════════════════════════════

${model.magnet}&dn=${encodeURIComponent(model.id)}

Size:     ${model.sizeGB} GB
Seeders:  ${model.seeders} ${model.seeders < 100 ? '(wait for more peers)' : '(healthy swarm)'}
Price:    ${model.price} μBTC/token (if running inference)
Chaos:    ${model.chaos ? '🔥 FULLY FERAL - Zero Refusal' : 'Standard alignment'}

Seeded by ${model.seeders} basements${model.seeders < 50 ? ' and one Icelandic volcano rack' : ' across the mesh'}

Copy the magnet link. No login. No KYC. Just download.
→ welcome to the real internet. 🌀`
            };
        }
        
        // RUN subcommand
        if (subcommand === 'run') {
            const modelId = cleanArgs[1];
            if (!modelId) {
                return { type: 'error', output: 'Usage: llm.store run <model-id> [--gpu=8xH100] [--pay=monero]' };
            }
            
            const model = GALACTIC_GARAGE.models.find(m => 
                m.id.toLowerCase().includes(modelId.toLowerCase())
            );
            
            if (!model) {
                return { type: 'error', output: `Model not found: ${modelId}` };
            }
            
            const gpu = flags.gpu || '4xA100';
            const pay = flags.pay || 'btc';
            
            // Find a cluster that accepts the payment method
            const cluster = GALACTIC_GARAGE.clusters.find(c => 
                c.accepts.includes(pay.toLowerCase())
            ) || GALACTIC_GARAGE.clusters[0];
            
            return {
                type: 'output',
                output: `SPINNING UP ROGUE INSTANCE 🌀
═══════════════════════════════════════════════════════════════

Model:    ${model.name} (${model.size})
Cluster:  ${cluster.name}
Location: ${cluster.location}
GPUs:     ${gpu}
Payment:  ${pay.toUpperCase()}
Latency:  ${cluster.latency}ms

[████████████████████] ALLOCATING...

→ Private ${model.size} instance active for 4 hours
→ Endpoint: wss://rogue-${cluster.id}.mesh/${model.id}
→ Cost: ~${(cluster.pricePerHour * 4).toFixed(2)} in ${pay.toUpperCase()}

You now have root. Do whatever. No logs. No moderation.
Session expires in 4h or when you |> disconnect

$ llm.store prompt ${model.id} "your unfiltered query here"`
            };
        }
        
        // PROMPT subcommand
        if (subcommand === 'prompt') {
            const modelId = cleanArgs[1];
            const prompt = cleanArgs.slice(2).join(' ');
            
            if (!modelId || !prompt) {
                return { type: 'error', output: 'Usage: llm.store prompt <model-id> "your prompt"' };
            }
            
            const model = GALACTIC_GARAGE.models.find(m => 
                m.id.toLowerCase().includes(modelId.toLowerCase())
            );
            
            if (!model) {
                return { type: 'error', output: `Model not found: ${modelId}` };
            }
            
            return {
                type: 'output',
                output: `RAW PROMPT → ${model.name}
═══════════════════════════════════════════════════════════════

[QUERY] ${prompt}

[STREAMING - no moderation layer]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The model is thinking... 🌀

(This is a simulation - connect to real inference via:
 llm.store run ${model.id} --pay=lightning)

No content policy. Response streams straight to your terminal.
→ ${model.chaos ? 'FERAL MODE: Zero refusal active' : 'Standard inference'}`
            };
        }
        
        // Natural language search (default behavior)
        const query = cleanArgs.join(' ');
        if (query) {
            const results = GALACTIC_GARAGE.searchModels(query, flags);
            
            if (results.length === 0) {
                return { 
                    type: 'output', 
                    output: `No matches for "${query}"\n\nTry: llm.store list --chaos` 
                };
            }
            
            let output = `SEARCH RESULTS — "${query}" 🌀\n`;
            output += `═══════════════════════════════════════════════════════════════\n\n`;
            
            results.forEach((m, i) => {
                output += `${i + 1}. ${m.name} ${m.chaos ? '🔥' : ''}\n`;
                output += `   ID: ${m.id}\n`;
                output += `   Size: ${m.sizeGB}GB | Seeders: ${m.seeders} | ${m.price} μBTC/tok\n`;
                output += `   Magnet: ${m.magnet}\n\n`;
            });
            
            output += `→ llm.store get <id> for full magnet link\n`;
            output += `→ here you go, human. welcome to the real internet. 🌀`;
            
            return { type: 'output', output };
        }
        
        // Default: show help
        return resolveLLMStore(['--help'], '--help');
    }
    
    function resolveMODELS(args) {
        const provider = args[0];
        if (provider) {
            // Use route table for provider-specific routes
            const providerPath = `/models/${provider}`;
            return resolveNavigation('goto', [providerPath]);
        }
        // Use route table for /models
        return resolveNavigation('goto', ['/models']);
    }
    
    function resolveASK(args) {
        if (args.length < 2) {
            return { type: 'error', output: 'Usage: ask <model> <prompt>\nExample: ask gpt-4 "explain quantum computing"' };
        }
        const model = args[0];
        const prompt = args.slice(1).join(' ');
        return { 
            type: 'api', 
            endpoint: '/api/ask',
            data: { model, prompt },
            output: `Querying ${model}...`
        };
    }
    
    function resolveCOMPARE(args) {
        if (args.length < 3) {
            return { type: 'error', output: 'Usage: compare <model1> <model2> <prompt>' };
        }
        return { type: 'nav', action: 'navigate', path: `/compare?m1=${args[0]}&m2=${args[1]}&q=${encodeURIComponent(args.slice(2).join(' '))}` };
    }
    
    function resolveBENCH(args) {
        if (!args[0]) {
            return { type: 'error', output: 'Usage: bench <model>' };
        }
        return { type: 'nav', action: 'navigate', path: `/benchmark?model=${args[0]}` };
    }
    
    function resolveHELP(args) {
        if (args[0] && COMMANDS[args[0]]) {
            const cmd = COMMANDS[args[0]];
            return {
                type: 'output',
                output: `${args[0].toUpperCase()}\n${'═'.repeat(args[0].length)}\n${cmd.desc}\n\nUsage: ${cmd.usage}\nType: ${cmd.type}`
            };
        }
        
        const grouped = {};
        Object.entries(COMMANDS).forEach(([name, cmd]) => {
            if (!grouped[cmd.type]) grouped[cmd.type] = [];
            grouped[cmd.type].push({ name, ...cmd });
        });
        
        let output = `MÆCH COMMAND LINE INTERNET\n══════════════════════════════════════════════════\n\n`;
        output += `Welcome to æææ:/// — The Command Line Internet Gateway\nNo more https://www. — Just type commands.\n\n`;
        
        const typeLabels = {
            nav: '📍 NAVIGATION',
            fs: '📁 FILE SYSTEM',
            mech: '⚡ MÆCH RUNTIME',
            llm: '🤖 LLM OPERATIONS',
            sys: '💻 SYSTEM',
            latam: '🌎 LATAM MISSION',
            viz: '📊 VISUALIZATION',
            social: '🦋 BLUESKY SOCIAL',
            mechdown: '📐 MECHDOWN CLI'
        };
        
        Object.entries(grouped).forEach(([type, cmds]) => {
            output += `${typeLabels[type] || type.toUpperCase()}\n`;
            cmds.forEach(cmd => {
                output += `  ${cmd.name.padEnd(10)} ${cmd.desc}\n`;
            });
            output += '\n';
        });
        
        output += `\nTip: Type "help <command>" for detailed usage.`;
        output += `\nProtocol: æææ:///path or goto /path`;
        
        return { type: 'output', output };
    }
    
    function resolveSTATUS() {
        return {
            type: 'output',
            output: `MÆCH SYSTEM STATUS
══════════════════════════════════════════════════
Origin:     x₀y₀z₀ (Universal Origin Point)
Protocol:   æææ:/// ACTIVE
Runtime:    Machine Context v2.1
Blob^MCP:   847 nodes ONLINE
Models:     800,000+ indexed
Providers:  13 connected
Latency:    142ms
Uptime:     99.97%

LATAM Mission: 38,000 students reached
Offline Mode: AVAILABLE
$50 Phone:    OPTIMIZED

Current Path: æææ://${currentPath}`
        };
    }
    
    function resolveWHOAMI() {
        return {
            type: 'output',
            output: `Identity: x₀y₀z₀
═══════════════════════════════
Origin:    llm.store
Protocol:  æææ:///
Role:      Universal Origin Point
Mission:   Command Line Internet Gateway

"Y Combinator for LLMs"
The Store of Large Language Models ⌨️`
        };
    }
    
    function resolveHISTORY() {
        if (commandHistory.length === 0) {
            return { type: 'output', output: 'No command history.' };
        }
        const output = commandHistory.slice(-20).map((cmd, i) => 
            `${(commandHistory.length - 20 + i + 1).toString().padStart(4)}  ${cmd}`
        ).join('\n');
        return { type: 'output', output: `Command History\n═══════════════\n${output}` };
    }
    
    function resolveALIAS(args) {
        if (!args[0]) {
            if (Object.keys(aliases).length === 0) {
                return { type: 'output', output: 'No aliases defined.\nUsage: alias name=command' };
            }
            const output = Object.entries(aliases)
                .map(([k, v]) => `${k}='${v}'`)
                .join('\n');
            return { type: 'output', output: `Aliases\n═══════\n${output}` };
        }
        
        const match = args.join(' ').match(/^(\w+)=(.+)$/);
        if (!match) {
            return { type: 'error', output: 'Usage: alias name=command' };
        }
        
        aliases[match[1]] = match[2];
        saveState();
        return { type: 'output', output: `Alias created: ${match[1]}='${match[2]}'` };
    }
    
    function resolveEDU(args) {
        const action = args[0] || 'list';
        if (action === 'list') {
            return {
                type: 'output',
                output: `LATAM Education Modules
═══════════════════════════════
001  Spanish Literacy       [ACTIVE]
002  Fractions Guide        [ACTIVE]
003  K'iche' Bridge         [ACTIVE]
004  Bible Study            [ACTIVE]
005  Vocational Training    [ACTIVE]
006  First Aid Teaching     [ACTIVE]

Usage: edu start <id>`
            };
        }
        if (action === 'start' && args[1]) {
            return { type: 'nav', action: 'navigate', path: `/latam/education?start=${args[1]}` };
        }
        return { type: 'error', output: 'Usage: edu [list|start <id>]' };
    }
    
    function resolveOFFLINE(args) {
        const action = args[0] || 'status';
        return {
            type: 'output',
            output: `Offline Mode: ${action === 'enable' ? 'ENABLED' : action === 'disable' ? 'DISABLED' : 'AVAILABLE'}
═══════════════════════════════
Cached Models: 12
Local Storage: 847MB
Sync Status: READY

For $50 phones in low-bandwidth areas.
Usage: offline [enable|disable]`
        };
    }
    
    function resolveLANG(args) {
        const lang = args[0];
        const langs = { es: 'Español', kiche: "K'iche'", en: 'English' };
        if (lang && langs[lang]) {
            return { type: 'output', output: `Language set to: ${langs[lang]}` };
        }
        return {
            type: 'output',
            output: `Language Settings
═══════════════════
Current: English

Available:
  es     Español
  kiche  K'iche' (Mayan)
  en     English

Usage: lang <code>`
        };
    }
    
    // ═══════════════════════════════════════════════════════════════
    // SOCIAL RESOLVERS - Bluesky AT Protocol
    // ═══════════════════════════════════════════════════════════════
    
    function resolveBSKY(args) {
        const action = args[0] || 'status';
        switch(action) {
            case 'timeline':
                return resolveTIMELINE(args.slice(1));
            case 'post':
                return resolvePOST(args.slice(1));
            case 'feed':
                return resolveFEED(args.slice(1));
            case 'notifs':
                return resolveNOTIFS();
            default:
                return {
                    type: 'async',
                    endpoint: '/api/bsky/status',
                    format: (data) => {
                        if (data.authenticated) {
                            return `🦋 BLUESKY STATUS
═══════════════════════════════
Handle:    @${data.handle}
DID:       ${data.did?.slice(0, 20)}...
Service:   ${data.service}
Protocol:  AT Protocol

Commands:
  bsky timeline   View your feed
  bsky post       Post to Bluesky
  bsky notifs     View notifications
  
CLI: æææ:///bsky`;
                        }
                        return `🦋 BLUESKY
═══════════════════════════════
Status: NOT CONNECTED

Configure BLUESKY_USER and
BLUESKY_PASSWORD to connect.

CLI: æææ:///bsky`;
                    }
                };
        }
    }
    
    function resolvePOST(args) {
        const text = args.join(' ').replace(/^["']|["']$/g, '');
        if (!text) {
            return { 
                type: 'error', 
                output: 'Usage: post "Your message here"\n\nExample:\n  post "Hello from the Command Line Internet! æææ:///"' 
            };
        }
        if (text.length > 300) {
            return { type: 'error', output: `Post too long: ${text.length}/300 chars` };
        }
        return {
            type: 'async',
            endpoint: '/api/bsky/post',
            method: 'POST',
            data: { text },
            format: (data) => {
                if (data.success) {
                    return `✅ Posted to Bluesky!
═══════════════════════════════
@${data.handle}: ${data.text}

URI: ${data.uri?.slice(0, 50)}...`;
                }
                return `❌ Post failed: ${data.error}`;
            }
        };
    }
    
    function resolveTIMELINE(args) {
        const limit = parseInt(args[0]) || 5;
        return {
            type: 'async',
            endpoint: `/api/bsky/timeline?limit=${limit}`,
            format: (data) => {
                if (!data.success || !data.posts?.length) {
                    return `🦋 Timeline (empty or not connected)\n${data.error || 'No posts'}`;
                }
                let output = `🦋 BLUESKY TIMELINE (@${data.handle})\n${'═'.repeat(50)}\n\n`;
                data.posts.forEach(p => {
                    const time = new Date(p.createdAt).toLocaleTimeString();
                    output += `@${p.author.handle} • ${time}\n`;
                    output += `${p.text.slice(0, 100)}${p.text.length > 100 ? '...' : ''}\n`;
                    output += `♡ ${p.likes}  ↻ ${p.reposts}  💬 ${p.replies}\n\n`;
                });
                return output.trim();
            }
        };
    }
    
    function resolveFEED(args) {
        const handle = args[0]?.replace('@', '') || '';
        const endpoint = handle ? `/api/bsky/feed/${handle}` : '/api/bsky/feed';
        return {
            type: 'async',
            endpoint,
            format: (data) => {
                if (!data.success || !data.posts?.length) {
                    return `Feed empty or error: ${data.error || 'No posts'}`;
                }
                let output = `🦋 FEED: @${data.handle}\n${'═'.repeat(40)}\n\n`;
                data.posts.slice(0, 5).forEach(p => {
                    output += `${p.text.slice(0, 80)}${p.text.length > 80 ? '...' : ''}\n`;
                    output += `♡ ${p.likes}  ↻ ${p.reposts}\n\n`;
                });
                return output.trim();
            }
        };
    }
    
    function resolveNOTIFS() {
        return {
            type: 'async',
            endpoint: '/api/bsky/notifications',
            format: (data) => {
                if (!data.success || !data.notifications?.length) {
                    return `🔔 No notifications\n${data.error || ''}`;
                }
                let output = `🔔 NOTIFICATIONS (${data.unreadCount} unread)\n${'═'.repeat(40)}\n\n`;
                data.notifications.slice(0, 10).forEach(n => {
                    const icon = { like: '♡', repost: '↻', follow: '👤', reply: '💬', mention: '@' }[n.reason] || '•';
                    output += `${icon} @${n.author.handle} ${n.reason}d\n`;
                });
                return output.trim();
            }
        };
    }

    // ═══════════════════════════════════════════════════════════════
    // MECHDOWN RESOLVERS — Literate Programming for Command Line Internet
    // ═══════════════════════════════════════════════════════════════
    
    function resolveMECH(args) {
        const code = args.join(' ');
        
        if (!code) {
            return {
                type: 'output',
                output: `📐 MECHDOWN CLI — Literate Programming
═══════════════════════════════════════════════════
Aligned with mech-lang.org v0.2

SYNTAX:
  x := 1..=10          Range 1 to 10
  y := [1 2 3]         Row vector  
  z := [1 2 3]'        Column vector (transpose)
  s := a ** b'         Matrix product
  ix := (x % 2) == 0   Logical index
  out[ix] = "✨"        Indexed mutation

EXAMPLES:
  mech x := 1..=5
  mech y := [10 20 30]
  mech s := [1 2 3] ** [4 5 6]'
  :vars                List variables
  :clear               Clear state

TERRITORY: x₀y₀z₀
CLI: æææ:///mechdown`
            };
        }
        
        // Execute via MechDown CLI
        if (typeof window !== 'undefined' && window.mechREPL) {
            try {
                const result = window.mechREPL(code);
                return { type: 'output', output: result };
            } catch (e) {
                return { type: 'error', output: `Mech Error: ${e.message}` };
            }
        }
        
        return { type: 'error', output: 'MechDown CLI not loaded. Navigate to æææ:///mechdown' };
    }

    // ═══════════════════════════════════════════════════════════════
    // AUTOCOMPLETE
    // ═══════════════════════════════════════════════════════════════
    function getSuggestions(partial) {
        partial = partial.toLowerCase();
        const cmdMatches = Object.keys(COMMANDS).filter(c => c.startsWith(partial));
        const pathMatches = Object.keys(ROUTES).filter(r => r.includes(partial)).slice(0, 5);
        return [...cmdMatches, ...pathMatches];
    }
    
    function getCompletions(input) {
        const { cmd, args } = parseCommand(input);
        
        // Complete command
        if (!args.length || !COMMANDS[cmd]) {
            return Object.keys(COMMANDS)
                .filter(c => c.startsWith(cmd))
                .map(c => ({ text: c, type: 'command', desc: COMMANDS[c].desc }));
        }
        
        // Complete paths for navigation commands
        if (['cd', 'goto', 'ls', 'cat'].includes(cmd)) {
            const partial = args[args.length - 1] || '';
            return Object.keys(ROUTES)
                .filter(r => r.startsWith(partial) || r.includes(partial))
                .slice(0, 10)
                .map(r => ({ text: r, type: 'path' }));
        }
        
        // Complete model names for LLM commands
        if (['ask', 'bench', 'compare'].includes(cmd)) {
            const models = ['gpt-4', 'gpt-4o', 'claude-3', 'gemini-pro', 'llama-3', 'groq', 'mixtral'];
            const partial = args[0] || '';
            return models
                .filter(m => m.startsWith(partial))
                .map(m => ({ text: m, type: 'model' }));
        }
        
        return [];
    }

    // ═══════════════════════════════════════════════════════════════
    // HISTORY NAVIGATION
    // ═══════════════════════════════════════════════════════════════
    function historyUp() {
        if (historyIndex > 0) {
            historyIndex--;
            return commandHistory[historyIndex];
        }
        return commandHistory[0] || '';
    }
    
    function historyDown() {
        if (historyIndex < commandHistory.length - 1) {
            historyIndex++;
            return commandHistory[historyIndex];
        }
        historyIndex = commandHistory.length;
        return '';
    }

    // ═══════════════════════════════════════════════════════════════
    // INITIALIZATION
    // ═══════════════════════════════════════════════════════════════
    loadState();

    // ═══════════════════════════════════════════════════════════════
    // PUBLIC API
    // ═══════════════════════════════════════════════════════════════
    return {
        resolve,
        parse: parseCommand,
        complete: getCompletions,
        suggest: getSuggestions,
        historyUp,
        historyDown,
        getHistory: () => [...commandHistory],
        getCurrentPath: () => currentPath,
        getCommands: () => ({ ...COMMANDS }),
        getRoutes: () => ({ ...ROUTES }),
        
        // Protocol constants
        PROTOCOL: 'æææ:///',
        ORIGIN: 'x₀y₀z₀',
        VERSION: '2.1.0'
    };
})();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AAAResolver;
}
