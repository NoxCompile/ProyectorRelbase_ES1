from django.http import JsonResponse, Http404
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Dejamos que DRF genere su respuesta inicial
    response = exception_handler(exc, context)

    # Si hay una respuesta y su código es 404, traducimos el mensaje
    if response is not None and response.status_code == 404:
        response.data = {
            "error": "Recurso no encontrado",
            "detalle": "La ruta o el ID que intentas consultar no existe en la API."
        }
    return response

def custom_404_view(request, exception=None):
    if request.path.startswith('/api/'):
        return JsonResponse({
            "error": "Recurso no encontrado",
            "detalle": "La ruta o el ID que intentas consultar no existe en la API."
        }, status=404)
    return JsonResponse({"error": "Página web no encontrada."}, status=404)