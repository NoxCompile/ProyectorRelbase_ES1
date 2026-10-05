from rest_framework import permissions

from .views import tiene_rol  # mismos roles que las pantallas HTML (ES2)


class PermisosES2(permissions.BasePermission):
    """
    GET / HEAD / OPTIONS: cualquier usuario autenticado (admin, normal, viewer).
    POST:                 admin o normal.
    PUT / PATCH / DELETE: solo admin.
    """

    message = "Tu rol no tiene permiso para esta operación."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST":
            return tiene_rol(user, "admin") or tiene_rol(user, "normal")
        return tiene_rol(user, "admin")
