# Hermes Secret Source Bridge — Local System Architecture

Origin point: `privateclient.ai`

## Components

```text
+---------------------------+      localhost      +------------------------+
|  C:\æ\site\              |  <--------------->  | secret_source_bridge/  |
|  secret-source-bridge.html  POST /hermes/v1/secret   server.py / launcher.py |
|  secret-source-bridge-import-map.js |           | LocalBridgeSecretSource|
+---------------------------+                     +------------------------+
        | user input                                      |
        | mask/reveal/copy                          atomic JSON store
        v                                            v
+---------------------------+               ~/.hermes/secrets/local_bridge.json
| Hermes desktop / gateway  |                       |
| config/secrets.sources    |  <--- register / fetch --+
+---------------------------+
```

## Local contract

- browser UI talks only to `http://127.0.0.1:7890/hermes/v1/secret`
- backend exposes `add`, `update`, `remove`, `list`, `reveal`, `import_json`, `export_env`, `clear`, `stats`, `search_by_kind`, `bulk_upsert`, `rotate_note`
- plugin stores everything in `~/.hermes/secrets/local_bridge.json` with atomic `.tmp` rename
- env override: `HERMES_SECRET_BRIDGE_PATH`

## Launch

From `C:\æ\hermes-fork\secret_source_bridge`:

- `python -m secret_source_bridge.launcher`
- or `launch.bat` on Windows

Then open:

- `C:\æ\site\secret-source-bridge.html`

## Boundaries

- readonly: no uploads to remote URLs or cloud sync
- no raw secrets in docs, logs, or HTML payloads
- `.env` has precedence over browser store for immutable processes
- local HTML/backend system is the sovereign surface for `privateclient.ai`
