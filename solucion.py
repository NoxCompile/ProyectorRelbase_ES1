# solucion.py

# 1. Declaración de variables y captura de datos
# Lo que entrega input() es texto, por lo que convertimos a entero con int()
producto = input("Ingrese el nombre del producto (Relbase): ")
stock_actual = int(input("Ingrese el stock actual: "))
ventas_esperadas = int(input("Ingrese las ventas esperadas del mes: "))

# 2. Regla de decisión lógica (4 resultados)
# Orden crítico: Primero evaluamos si hay datos inválidos
if stock_actual < 0 or ventas_esperadas < 0:
    estado = "Dato Inválido: Las cantidades no pueden ser negativas."
elif stock_actual >= ventas_esperadas:
    estado = "Óptimo: El stock cubre las proyecciones del mes completo."
elif stock_actual >= (ventas_esperadas / 2):
    estado = "Alerta de Quincena: El stock solo cubre la primera mitad del mes."
else:
    # Si no es inválido, ni óptimo, ni alerta, por descarte es crítico
    estado = "Crítico: Requiere orden de compra urgente."

# 3. Mostrar el resultado
print(f"\n--- Resumen de Abastecimiento ---")
print(f"Producto: {producto}")
print(f"Estado: {estado}")