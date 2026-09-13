from django.contrib import admin
from .models import Registro

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    # Despliega estas columnas en la lista principal
    list_display = ("producto", "estado", "stock_actual", "ventas_esperadas", "fecha_consulta")
    
    # Habilita un panel lateral para filtrar rápidamente[cite: 5]
    list_filter = ("estado", "eliminado")
    
    # Habilita una barra de búsqueda[cite: 5]
    search_fields = ("producto",)
    
    # Protege campos sensibles contra modificaciones manuales[cite: 5]
    readonly_fields = ("fecha_eliminacion",)