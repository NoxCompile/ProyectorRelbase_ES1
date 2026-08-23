from django.contrib import admin
from django.urls import path
from core.views import resumen # Importamos la vista que creamos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', resumen, name='resumen'), # Ruta raíz apunta a nuestra vista
]
