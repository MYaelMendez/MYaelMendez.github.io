# æQR Vision MCP · 0.1.0

Servidor local compartido para clientes MCP con transporte stdio. Primera versión funcional; no es una integración instalada en Codex, Hermes o ChatGPT.

## Herramientas implementadas

| Herramienta | Resultado |
| --- | --- |
| `vision_status` | Capacidades disponibles y proveedores no conectados |
| `scan_qr` | Texto de QR, esquinas en píxeles, dimensiones y hashes |
| `calibration_reference` | Origen y punto fijo (1,1,1) en unidades locales abstractas |

Una observación incluye SHA-256 de la imagen cuando existe, SHA-256 del resultado y fecha UTC. Estos hashes permiten comparar contenido; no son firma, certificación, cadena persistente ni prueba de autorización. Los resultados señalan `authority_granted: false`.

## Instalación local

Desde este directorio, con Python 3.11 o posterior:

```sh
python -m venv .venv
.venv/bin/pip install -e '.[test]'
mkdir -p approved-images
AEQR_VISION_IMAGE_ROOT="$PWD/approved-images" .venv/bin/aeqr-vision-mcp
```

En Windows utiliza los ejecutables equivalentes de `.venv/Scripts`. El proceso usa stdio para MCP, no una interfaz de chat en consola. Ajusta las rutas absolutas de `mcp.example.json` en la configuración del cliente compatible. El esquema de configuración de cada cliente puede variar.

Solo se leen imágenes PNG/JPEG dentro de la carpeta configurada. Las rutas absolutas, escapes por `..` y symlinks externos son rechazados. Límites: 10 MiB y 16 megapíxeles. Usa una carpeta controlada por el principal, sin modificaciones concurrentes de terceros; esta implementación no pretende aislar un sistema de archivos hostil con carreras de symlinks.

Los payloads QR se devuelven como datos no confiables. No se siguen URLs, ejecutan instrucciones, solicitan cámaras, suben imágenes ni conceden credenciales. Quien conecta el cliente debe decidir qué imágenes y resultados puede leer el agente; pueden contener datos privados. No hay telemetría ni adaptadores externos implementados.

## Inspiración y adaptadores previstos

- [Roboflow Inference SDK](https://docs.roboflow.com/reference/inference/inference-sdk): cliente documentado para inferencia local, edge o alojada. Futuro adaptador requerirá endpoint, modelo y autorización del destino de las imágenes.
- [Robovision SDK](https://robovision.ai/no-code-computer-vision-solution/robovision-sdk): inspiración para ciclo de datos, modelos y despliegue industrial. Adaptador pendiente de contrato y acceso al SDK/API de la instalación del usuario.
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk): este prototipo usa la API estable 1.x FastMCP, limitada a `mcp<2`. Una actualización a SDK 2.x requiere revisar compatibilidad.

No hay asociación comercial o integración certificada con estos proveedores. No se inventan endpoints de Robovision. La referencia XYZ no estima pose 3D desde una imagen: eso requiere intrínsecos de cámara, tamaño físico de marcador, unidades y mediciones independientes. Tampoco verifica identidad biométrica.

## Validación

```sh
.venv/bin/python -m unittest discover -s tests -v
```

Resultado local: 4 pruebas aprobadas, con mcp 1.30.0, zxing-cpp 2.3.0 y Pillow 12.3.0 en Python 3.12.

Las pruebas incluyen lectura real de QR generado, hash de imagen, imágenes sin códigos, límites, escapes de rutas y sesión MCP stdio real con listado e invocación de las tres herramientas. No se probaron plataformas proveedoras ni configuración dentro de aplicaciones cliente.

GitHub Pages puede publicar la documentación y el mapa del plugin; no ejecuta el proceso Python. Un conector remoto requeriría hosting del servidor, autenticación y autorización adicionales. Esta versión se propone para revisión, sin despliegue remoto ni cambios de permisos.
