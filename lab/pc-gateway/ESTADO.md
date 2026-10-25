# >_ PC:// · Estado de continuación

Actualizado: 2026-10-22 00:30 CDT · Principal: Yæl · No hay secretos en este archivo; las llaves están en la bóveda.

## Qué es PC://
**La capa del principal**: identidad, autoridad, cobro y recibos. Los proveedores operan debajo de ella como capacidades; por ejemplo, doola es `capability://formation`.
Muchos agentes. Un principal. Evidence ≠ Authority.

## Qué hay en este repo (rama `lab`)
| Pieza | Ruta | Commit | Estado |
|---|---|---|---|
| Extensión Chromium v0.1 | `lab/pc-extension/v0/` | 0a9f487 | Demo live. Funciona en Chrome, Edge, Brave, Arc y Opera con "Load unpacked". Faltan los íconos de Wilhælm T. |
| Gateway v0.2 | `lab/pc-gateway/v0.2/` | 9b68171 | Node ≥18 sin dependencias. 19/19 pruebas contra el sandbox de doola. **No desplegado.** |
| Demo interactiva | `lab/pc-gateway/demo/` | 3fdc782 | Simulación: el agente pide, el principal aprueba, doola forma la empresa y cada paso queda en un recibo SHA-256. Usa las tarifas reales del sandbox. |

Demo: https://lutheraninstitute.github.io/aeee-lab/lab/pc-gateway/demo/

## Gateway v0.2 · garantías
- `pc_sk_`: la llave del principal, que vive solo en el servidor. `pc_ss_`: sesiones de agente cortas, limitadas y revocables.
- Todo POST lleva Idempotency-Key: repetir la misma petición es seguro, y reutilizar la llave con otro cuerpo devuelve 409.
- Los agentes no ejecutan acciones consecuentes; solo crean `required-actions`, y solo el principal aprueba o deniega.
- Los recibos son append-only y se encadenan con SHA-256 desde GENESIS.
- Los webhooks de doola llegan firmados con HMAC-SHA256 (`X-Doola-Signature`) y se reconcilian sin polling.
- Formato de respuesta `{payload, error}`, más `GET /v1/manifest` y `/llms.txt`.

## doola
- Sandbox: `https://api.test.doola.com`. La llave va cruda en `Authorization`, sin Bearer.
- Tarifas estatales para LLC (sandbox): Wyoming $100, Delaware $90, Texas $300.
- Oferta de Haliny: 33 formaciones a $150 = $4,950. Cada una incluye filing, EIN, agente registrado por un año y dirección virtual. Los créditos no expiran.
- **Reunión: 2026-11-23, 9:00–9:30 AM CST.** Tema: revisar y firmar el acuerdo.
- **No usar llaves live antes del acuerdo.**

### Puntos para negociar (nada enviado aún)
1. La integración PC:// ya está probada (19/19) y la demo está en línea.
2. Un canal agent-native, con PC:// como posible integración de referencia.
3. Cero pago inicial: $150 por cada formación vendida, o compensado con las primeras ventas. La propuesta es un canal, no un descuento.
4. Aclarar si la atribución va por API o por PartnerStack.

## Formación propia (desintermediar), análisis del 2026-10-22
- **Texas:** Form 205 por SOSDirect, $300. El agente registrado debe ser residente de TX o una entidad registrada en TX, con oficina física. Yæl vive en Texas y puede ser el agente, así que esto es viable ya.
- **Wyoming:** el agente necesita oficina física en WY y presencia en horario hábil. Con más de 10 entidades hay que registrarse como Commercial Registered Agent, con renovación cada 31 de diciembre. Lo práctico es un socio mayorista en WY.
- **EIN:** se puede tramitar como Third Party Designee, con una SS-4 firmada por el cliente y una declaración; el IRS no acepta firma electrónica para esa autorización. Sin SSN o ITIN, el trámite va por fax o teléfono.
- Lo que doola resuelve hoy: correo y notificaciones legales, reportes anuales, dirección virtual y rechazos del estado.
- Ruta sugerida: Texas propio para clientes del Valle; doola para WY, DE y fundadores sin SSN. **No mostrar esta carta antes del 23 de noviembre.**

## Ofertas
- #startabusiness · formación.
- **Consulta rápida con Yæl · banca privada**, precio por definir.
- Private Client · setup owner-only, desde $1,200.

## Infraestructura
- `privateclient.ai` está live en la droplet Hermes, con `/startabusiness`.
- Regla: un principal por droplet; nunca custodiar llaves de varios clientes en una misma droplet.
- Antes de desplegar el gateway, en este orden: 1) snapshot de la droplet, 2) firewall, 3) secretos en `/etc/privateclient/pc-gateway.env` (fuera del repo), 4) systemd, 5) Caddy/TLS, 6) webhook doola por HTTPS.

## Pendientes
- [ ] Precio de la consulta rápida.
- [ ] Íconos Wilhælm T para la extensión.
- [ ] Snapshot y firewall antes de tocar producción.
- [ ] Desplegar el gateway y configurar los webhooks.
- [ ] Opera Add-ons: reintentar cuando haya contraseña correcta de Google.
- [ ] Preparar la reunión del 23 de noviembre.
