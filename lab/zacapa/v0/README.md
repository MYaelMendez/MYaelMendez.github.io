# >_ZACAPA.DAO · v0 · primeros principios

Laboratorio Zacapa.ai · Instituto Luterano Latinoamericano

- 11 cabeceras municipales de Zacapa (OpenStreetMap / Nominatim, 2026-10-17).
- Matriz 11×11 de km y minutos reales por carretera (OSRM, 2026-10-17); horneada en la página: sin llaves ni API en el navegador.
- Red troncal = árbol de expansión mínima sobre km reales, dibujada con la geometría de carretera.
- Motor determinista (semilla): solicitudes municipio → cabecera, 06:00–18:00.
- Decisión humana: ACCESO (primero quien más espera) vs CAPACIDAD (primero el más cercano). ⚖️ COMPARAR muestra el costo de cada regla.
- Witness: cadena SHA-256 canónica desde GENESIS, sin marcas de tiempo; ✓ VERIFICAR la recalcula.

Escenario, no pronóstico. Sin tráfico, tarifas ni tiempos de abordaje. Votación demostrativa local.
Human stays root · Evidence ≠ Authority.

Datos © OpenStreetMap contributors, ODbL 1.0.
