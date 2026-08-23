import json
from django.shortcuts import render

# Esta es la vista que lee el JSON y lo envía al Template
def resumen(request):
    try:
        # Abrimos nuestro historial de abastecimiento
        with open("datos.json", "r") as f:
            registros = json.load(f)
    except FileNotFoundError:
        registros = [] # Si el archivo no existe, pasamos una lista vacía
    
    # Enviamos la variable 'registros' al template HTML
    return render(request, "resumen.html", {"registros": registros})