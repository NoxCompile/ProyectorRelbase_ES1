# Uso de Inteligencia Artificial (ia.md)

**1. Herramienta utilizada y propósito:**
Utilicé un asistente de IA basado en LLM (Gemini/ChatGPT) como copiloto para estructurar el archivo `plan.md` inicial y generar la estructura base de la regla de decisión en Python.

**2. Consulta concreta realizada:**
Prompt: *"Soy estudiante de programación back end. Quiero resolver este problema: En mi trabajo extraemos reportes de ventas del sistema Relbase, pero debo calcular manualmente en Excel cuánto stock necesitamos para cubrir el mes, perdiendo tiempo y arriesgando quiebres. Ayúdame a escribir un plan con dos apartados (Negocio y Técnico) y la priorización MoSCoW. Restricción: se resuelve con variables, if/elif, un archivo JSON y una sola vista Django. Sin base de datos."*

**3. Análisis crítico y corrección humana:**
La IA me entregó una buena estructura para el MoSCoW, pero cometió dos errores técnicos en su propuesta de código inicial que tuve que corregir manualmente:
* **El orden del algoritmo:** La IA posicionó el caso de éxito ("Óptimo") en el primer `if` y dejó el error de "Dato Inválido" al final del `else`. Corregí esto en mi archivo `solucion.py`, colocando la validación de números negativos (`stock_actual < 0`) en la parte superior del bloque `if`. Si no lo hacía, el programa habría procesado números falsos antes de atrapar el error.
* **Sobrescritura de datos:** La IA sugirió un script que sobreescribía el archivo JSON en cada ejecución. Tuve que importar la librería `os` en Python e implementar `os.path.exists()` para cargar el historial anterior, hacer un `.append()` del nuevo registro, y recién ahí volver a guardar, logrando un historial real que luego inyecté a la vista de Django.