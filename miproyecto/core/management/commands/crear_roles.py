from decouple import config
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

# usuario -> (grupo, variable del .env con su contraseña)
USUARIOS = {
    "admin_api": ("admin", "PASS_ADMIN"),
    "normal_api": ("normal", "PASS_NORMAL"),
    "viewer_api": ("viewer", "PASS_VIEWER"),
}


class Command(BaseCommand):
    help = "Crea los grupos admin/normal/viewer y un usuario por rol (claves desde .env, sin valores por defecto)."

    def handle(self, *args, **kwargs):
        for _, (grupo, _var) in USUARIOS.items():
            Group.objects.get_or_create(name=grupo)
            self.stdout.write(f"Grupo {grupo} asegurado.")

        for username, (grupo, var) in USUARIOS.items():
            clave = config(var, default="")
            if not clave:
                self.stdout.write(self.style.WARNING(
                    f"Falta {var} en .env: no se crea el usuario {username}."))
                continue
            user, creado = User.objects.get_or_create(username=username)
            user.set_password(clave)  # también actualiza la clave si el usuario ya existía
            user.save()
            user.groups.set([Group.objects.get(name=grupo)])
            self.stdout.write(self.style.SUCCESS(
                f"Usuario {username} {'creado' if creado else 'actualizado'} con rol {grupo}."))
