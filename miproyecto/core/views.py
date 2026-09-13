from django.shortcuts import render, redirect, get_object_or_404
from solucion import decidir
from .models import Registro

# READ
def lista(request):
    registros = Registro.objects.filter(eliminado=False)
    return render(request, "resumen.html", {"registros": registros})

# CREATE
def crear(request):
    error = None
    if request.method == "POST":
        producto = request.POST.get("producto", "").strip()
        try:
            stock = int(request.POST.get("stock_actual", ""))
            ventas = int(request.POST.get("ventas_esperadas", ""))
            estado_calculado = decidir(stock, ventas)
            
            Registro.objects.create(
                producto=producto,
                stock_actual=stock,
                ventas_esperadas=ventas,
                estado=estado_calculado
            )
            return redirect("lista")
        except ValueError:
            error = "El stock y las ventas deben ser números enteros."
            
    return render(request, "form.html", {"accion": "Crear", "error": error})

# UPDATE
def editar(request, pk):
    reg = get_object_or_404(Registro, pk=pk, eliminado=False)
    error = None
    if request.method == "POST":
        reg.producto = request.POST.get("producto", "").strip()
        try:
            reg.stock_actual = int(request.POST.get("stock_actual", ""))
            reg.ventas_esperadas = int(request.POST.get("ventas_esperadas", ""))
            
            # Recalcular siempre el estado al editar para no dejar datos corruptos
            reg.estado = decidir(reg.stock_actual, reg.ventas_esperadas)
            reg.save()
            return redirect("lista")
        except ValueError:
            error = "Cantidades inválidas."
            
    return render(request, "form.html", {"accion": "Editar", "registro": reg, "error": error})

# DELETE
def eliminar(request, pk):
    reg = get_object_or_404(Registro, pk=pk, eliminado=False)
    if request.method == "POST":
        reg.soft_delete() # Aplicamos el borrado lógico definido en el modelo
        return redirect("lista")
    return render(request, "confirmar.html", {"registro": reg})