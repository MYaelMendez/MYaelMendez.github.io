# PC:// · Wilhælm T — extensión v0.1 (lab · DEMO)

Resolver de PrivateClient: **æQR → email y email → æQR**. Solo lectura. Many agents. One principal.

## Instalar (Chromium: Chrome, Edge, Brave, Arc, Opera)
1. Descarga esta carpeta (`lab/pc-extension/v0/`).
2. Abre `chrome://extensions` (Edge: `edge://extensions`, Opera: `opera://extensions`, Brave: `brave://extensions`).
3. Activa el **Modo desarrollador** y luego elige **Cargar descomprimida**. Selecciona la carpeta.

## Usar
- En la barra, escribe `pc`, un espacio y la dirección: `wilhælm.t`, `æ://llm.store/hermes` o `hermes@llm.store`.
- También funciona el ícono (popup), el panel lateral (Chrome/Edge/Brave) y la página web de este folder.
- En enlaces, Chromium solo acepta esquemas propios con `web+`, así que `PC://x` se escribe `web+pc://x`.

## Reglas
- DEMO conceptual: los æQR no son escaneables todavía. El registro (`registry.json`, `ae.mail/0.1`) es un borrador.
- Sin secretos y sin permisos de red más allá de su propio paquete. No envía correo.
- Evidence ≠ Authority: el resolver informa, el humano decide. Los cambios entran por PR aprobado por Yæl.
