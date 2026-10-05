from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .models import Registro
from .serializers import RegistroSerializer
from .permissions import PermisosES2
from solucion import decidir

class RegistroViewSet(viewsets.ModelViewSet):
    serializer_class = RegistroSerializer
    permission_classes = [PermisosES2]

    def get_queryset(self):
        # Filtra borrado lógico
        qs = Registro.objects.filter(eliminado=False).order_by("-fecha_consulta")
        
        # Filtro opcional por estado
        estado = self.request.query_params.get('estado', None)
        if estado:
            estados_validos = dict(Registro.ESTADO_CHOICES).keys()
            if estado not in estados_validos:
                # Lanzar error 400 si el estado no existe
                raise ValidationError({"estado": f"Valor inválido. Opciones: {', '.join(estados_validos)}"})
            qs = qs.filter(estado=estado)
        return qs

    def perform_create(self, serializer):
        stock = serializer.validated_data["stock_actual"]
        ventas = serializer.validated_data["ventas_esperadas"]
        # Calcula el estado usando tu regla
        estado_calculado = decidir(stock, ventas)
        serializer.save(estado=estado_calculado)

    def perform_update(self, serializer):
        # Aseguramos que PUT/PATCH recalculen el estado
        instance = serializer.instance
        stock = serializer.validated_data.get("stock_actual", instance.stock_actual)
        ventas = serializer.validated_data.get("ventas_esperadas", instance.ventas_esperadas)
        estado_calculado = decidir(stock, ventas)
        serializer.save(estado=estado_calculado)

    def perform_destroy(self, instance):
        instance.soft_delete()