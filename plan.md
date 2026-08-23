# Plan del Proyecto: Proyector de Abastecimiento (Relbase)

## 1. Apartado de Negocio
* **Problema:** Actualmente, calculo manualmente en Excel cuánto stock necesitamos para cubrir inicio, mitad y final de mes basándome en reportes de Relbase, perdiendo tiempo y arriesgando quiebres.
* **Solución:** Un sistema automatizado que evalúa el stock actual de un producto frente a su proyección de ventas, devolviendo su estado de abastecimiento.
* **Alcance:** El sistema evaluará el estado de un solo producto a la vez.
* **MoSCoW:**
  * **Must (MVP):** Capturar nombre, stock y ventas esperadas. Evaluar con una regla de 4 estados. Guardar en JSON y mostrar tabla.
  * **Should:** Permitir cargar un CSV con múltiples productos.
  * **Could:** Enviar alerta por correo en estado crítico.
  * **Won't:** Base de datos relacional y login de usuarios.

## 2. Apartado Técnico
* **Datos de Entrada:** `producto` (texto), `stock_actual` (entero), `ventas_esperadas` (entero).
* **Regla de Decisión:**
  1. *Dato Inválido:* `stock_actual < 0` o `ventas_esperadas < 0`.
  2. *Óptimo:* `stock_actual >= ventas_esperadas`.
  3. *Alerta de Quincena:* `stock_actual >= (ventas_esperadas / 2)` y `< ventas_esperadas`.
  4. *Crítico:* `stock_actual < (ventas_esperadas / 2)`.
* **Paquete Externo:** `tabulate` para mostrar el resumen en tabla.
* **Pantalla Web:** Una vista de Django leyendo el archivo JSON.