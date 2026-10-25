# DAOLLC.ai · LAB v0 · gobernanza simulada

Laboratorio æ:// · Instituto Luterano Latinoamericano · #OSW

**DEMO · simulación · no es asesoría legal ni despliega contratos.**

`>_æ:#startabusiness → ORGANIZE → capability://formation → LLC://ACTIVE`

Una DAO LLC ficticia (5 miembros, semilla 2026, banco de 100,000 USDx) con dos motores de gobernanza sobre la misma lista de propuestas, el mismo padrón y el mismo banco:

- **MOLOCH v2** (port de [MolochVentures/moloch](https://github.com/MolochVentures/moloch), `Moloch.sol`): submit → sponsor (depósito en escrow) → voto Sí/No sólo con shares → gracia → process en orden de cola. Shares vs loot, banco del gremio, ragequit proporcional (fairShare), guildKick → jail (shares → loot) → ragekick, dilutionBound, recompensa de procesamiento, patrón pull (withdraw).
- **GOVERNOR** (port de [OpenZeppelin governance](https://github.com/OpenZeppelin/openzeppelin-contracts/tree/master/contracts/governance)): Pending → Active → Defeated/Succeeded → Queued → Executed (y Canceled; Expired estilo Compound tras la ventana del timelock). votingDelay, votingPeriod, snapshot de peso, CountingSimple (For/Against/Abstain; quorum cuenta For + Abstain), quorum fraccional, TimelockController (Unset → Waiting → Ready → Done, minDelay). proposalId = hash del contenido.

**HUMAN://** · process, execute, ragequit, ragekick y withdraw requieren autorización humana: pulsar la acción, escribir `APRUEBO` y confirmar con un toque real. El permiso es un objeto opaco de un solo uso ligado a la acción exacta; `execute(id, true)` no autoriza nada. æsymov y los agentes sólo leen y recomiendan.

**Witness** · eventos JSON canónicos encadenados con SHA-256 desde `GENESIS`, sin marcas de tiempo; Verificar recalcula la cadena; Export JSON la descarga.

**Para agentes** · `window.DAOLLC` (sólo lectura: `state`, `summary()`, `verify()`, `witness()`) y `?agent` (resumen en texto plano).

## Diferencias deliberadas con los contratos

- Reloj simulado en bloques (1 bloque = 1 periodo Moloch); nada espera tiempo real.
- SHA-256 en lugar de keccak256 para ids y operaciones.
- Un solo token (USDx); sin whitelist de tokens ni delegateKey.
- `highestIndexYesVote = -1` cuando un miembro nunca votó Sí (Moloch usa 0).
- En Governor, sólo proponen y votan cuentas con peso > 0.

La envoltura LLC se explica como mapa conceptual (idea MolochLAO). Formar una LLC real requiere abogado y agente registrado; esto sólo simula gobernanza.

Human stays root · Evidence ≠ Authority · Humans decide, agents relay.

Patrones de código abierto: Moloch (MIT) · OpenZeppelin Contracts (MIT).
