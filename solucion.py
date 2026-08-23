import json
import os
from tabulate import tabulate

# 1. Declaración de variables y captura de datos
producto = input("Ingrese el nombre del producto (Relbase): ")
stock_actual = int(input("Ingrese el stock actual: "))
ventas_esperadas = int(input("Ingrese las ventas esperadas del mes: "))

# 2. Regla de decisión lógica (4 resultados)
if stock_actual < 0 or ventas_esperadas < 0:
    estado = "Dato Inválido: Cantidades negativas."
elif stock_actual >= ventas_esperadas:
    estado = "Óptimo: Cubre el mes completo."
elif stock_actual >= (ventas_esperadas / 2):
    estado = "Alerta: Cubre solo primera quincena."
else:
    estado = "Crítico: Requiere compra urgente."

# 3. Preparar el diccionario con el registro actual
nuevo_registro = {
    "Producto": producto,
    "Stock": stock_actual,
    "Ventas": ventas_esperadas,
    "Estado": estado
}

# 4. Lógica de persistencia en archivo JSON
archivo_json = "datos.json"
registros = []

# Si el archivo ya existe, cargamos su contenido anterior
if os.path.exists(archivo_json):
    with open(archivo_json, "r") as archivo:
        registros = json.load(archivo)

# Añadimos la consulta actual a la lista
registros.append(nuevo_registro)

# Sobrescribimos el archivo JSON con la lista actualizada
with open(archivo_json, "w") as archivo:
    json.dump(registros, archivo, indent=4)

# 5. Mostrar el resultado formateado en consola
print("\n--- Historial de Abastecimiento Relbase ---")
print(tabulate(registros, headers="keys", tablefmt="grid"))