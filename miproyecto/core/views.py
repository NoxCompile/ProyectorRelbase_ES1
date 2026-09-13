from django.shortcuts import render, redirect, get_object_or_404
from solucion import decidir
from .models import Registro
from django.contrib.auth import authenticate, login, logout
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def tiene_rol(user, *roles):
    # Verifica si el usuario pertenece al grupo o si es superusuario (admin total)
    return user.groups.filter(name__in=roles).exists() or user.is_superuser

def requiere_rol(*roles):
    def decorador(view_func):
        @wraps(view_func)
        @login_required(login_url="login")
        def wrapper(request, *args, **kwargs):
            if tiene_rol(request.user, *roles):
                return view_func(request, *args, **kwargs)
            # Si no tiene el rol, se le bloquea el paso y se le devuelve a la lista
            messages.error(request, "No tienes permiso para esta acción.")
            return redirect("lista")
        return wrapper
    return decorador

# READ
@login_required(login_url="login")
def lista(request):
    registros = Registro.objects.filter(eliminado=False)
    return render(request, "resumen.html", {"registros": registros})

# CREATE
@requiere_rol("admin", "normal")
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
@requiere_rol("admin")
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
@requiere_rol("admin")
def eliminar(request, pk):
    reg = get_object_or_404(Registro, pk=pk, eliminado=False)
    if request.method == "POST":
        reg.soft_delete() # Aplicamos el borrado lógico definido en el modelo
        return redirect("lista")
    return render(request, "confirmar.html", {"registro": reg})

def vista_login(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", "")
        )
        if user:
            login(request, user)
            return redirect("lista")
        
        messages.error(request, "Usuario o contraseña incorrectos.")
    
    return render(request, "login.html")

def vista_logout(request):
    logout(request)
    return redirect("login")