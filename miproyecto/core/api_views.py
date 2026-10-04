from rest_framework import viewsets
from .models import Registro
from .serializers import RegistroSerializer
from .permissions import SoloStaffBorra

class RegistroViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.filter(eliminado=False).order_by("-fecha_consulta")
    serializer_class = RegistroSerializer
    permission_classes = [SoloStaffBorra]

    def perform_create(self, serializer):
        stock = serializer.validated_data["stock_actual"]
        ventas = serializer.validated_data["ventas_esperadas"]
        
        estado_calculado = "Invalido"
        if ventas > 0:
            if stock >= ventas:
                estado_calculado = "Optimo"
            elif stock >= ventas // 2:
                estado_calculado = "Alerta"
            else:
                estado_calculado = "Critico"

        serializer.save(estado=estado_calculado)

    def perform_destroy(self, instance):
        instance.soft_delete()