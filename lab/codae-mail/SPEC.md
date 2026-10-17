# Codæ Mail · SPEC v0.1 (lab)

**Idea de Yæl (2026-10-16):** Codæ Mode por correo. El correo más viejo de internet, convertido en terminal soberana.
Tarjeta: `LutheranInstitute/Cli.llc` → `cards/008-hermes-correo.md`.

| Correo | Codæ Mode |
|---|---|
| Asunto | el `>_` prompt (intención tipada) |
| Cuerpo | contexto |
| Respuesta de Hermes | recibo con evidencia |
| Hilo | bitácora de la sesión |

## 1 · Gramática del asunto ("asuntos æ")
```
[æ:<tarjeta>] <verbo> <objeto…> [#clase]
tarjeta := 3 dígitos (008) | "new"
verbo   := ping | status | read | summarize | draft | prepare | run | review
clase   := #consulta | #preparar | #ejecutar   (si falta, se infiere del verbo)
```
Ejemplos: `[æ:008] ping` · `[æ:007] status v/GEN` · `[æ:007] prepare PR segment.py #preparar` · `[æ:new] idea correo como terminal`.

| verbo | clase inferida |
|---|---|
| ping, status, read, summarize | consulta |
| draft, prepare, review | preparar |
| run | ejecutar |

## 2 · Puertas (en orden)
1. **Remitente**: está en `EMAIL_ALLOWED_USERS`; si no, se ignora en silencio.
2. **Gramática**: el asunto parsea; si no, Hermes responde con la ayuda.
3. **Tarjeta**: existe en `Cli.llc/cards/`; `[æ:new]` crea una en `triage` y no ejecuta nada más.
4. **Estado**: `#ejecutar` solo si la tarjeta está en `ready`.
5. **Autoridad**: dinero, borrar, publicar, secretos, correos a terceros, compromisos legales → Hermes responde `HOLD · requiere Yæl` y espera una respuesta `APROBADO <recibo>` del mismo hilo.
6. **Secretos**: si el cuerpo trae algo con forma de llave o contraseña, Hermes no la usa, responde `RECHAZADO · secreto en correo` y pide rotarla.

## 3 · Recibo (respuesta de Hermes, en el mismo hilo)
```
>_ recibo æ:<tarjeta>-<aaaammdd>-<n>
clase:      consulta | preparar | ejecutar
puerta:     PASS | HOLD | RECHAZADO
estado:     tarjeta <id> → <estado>
cambios:    <archivos / PR / ninguno>
evidencia:  sha256:<hash del cuerpo del recibo>
siguiente:  <qué decide Yæl>
```
*Evidence ≠ Authority: el recibo informa, Yæl decide.*
