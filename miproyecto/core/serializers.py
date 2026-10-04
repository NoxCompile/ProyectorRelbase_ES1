from rest_framework import serializers
from .models import Registro

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registro
        fields = [
            "id", 
            "producto", 
            "stock_actual", 
            "ventas_esperadas", 
            "estado", 
            "fecha_consulta"
        ]
        read_only_fields = ["estado", "fecha_consulta"]

    def validate_stock_actual(self, valor):
        if valor < 0:
            raise serializers.ValidationError("El stock actual no puede ser negativo.")
        return valor

    def validate_ventas_esperadas(self, valor):
        if valor < 0:
            raise serializers.ValidationError("Las ventas esperadas no pueden ser negativas.")
        return valor