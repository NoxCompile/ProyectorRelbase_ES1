from django.db import models
from django.utils import timezone

class Registro(models.Model):
    # Definimos los estados exactos que arroja nuestra regla de negocio
    ESTADO_CHOICES = [
        ('Optimo', 'Óptimo (Cubre mes)'),
        ('Alerta', 'Alerta de Quincena'),
        ('Critico', 'Crítico (Urgente)'),
        ('Invalido', 'Dato Inválido')
    ]
    
    producto = models.CharField(max_length=100)
    stock_actual = models.IntegerField()
    ventas_esperadas = models.IntegerField()
    # Usamos choices para que la base de datos valide por nosotros
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    fecha_consulta = models.DateTimeField(default=timezone.now)
    
    # Borrado lógico: no se pierde nada, solo se oculta
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha_consulta"]

    def __str__(self):
        return f"{self.producto} - {self.estado}"

    def soft_delete(self):
        """Marca el registro como eliminado sin borrarlo de la base de datos."""
        self.eliminado = True
        self.fecha_eliminacion = timezone.now()
        self.save() # Sin esto no guarda nada