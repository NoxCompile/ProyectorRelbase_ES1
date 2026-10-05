from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User, Group
from solucion import decidir
from .models import Registro

class APIRegistroTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Crear grupos
        self.group_admin = Group.objects.create(name='admin')
        self.group_normal = Group.objects.create(name='normal')
        self.group_viewer = Group.objects.create(name='viewer')

        # Crear usuarios
        self.user_admin = User.objects.create_user(username='admin', password='123')
        self.user_admin.groups.add(self.group_admin)

        self.user_normal = User.objects.create_user(username='normal', password='123')
        self.user_normal.groups.add(self.group_normal)

        self.user_viewer = User.objects.create_user(username='viewer', password='123')
        self.user_viewer.groups.add(self.group_viewer)

        # Crear un registro de prueba
        self.registro = Registro.objects.create(producto="Teclado", stock_actual=10, ventas_esperadas=5, estado="Optimo")
        self.url_list = reverse('registro-list')
        self.url_detail = reverse('registro-detail', kwargs={'pk': self.registro.pk})

    def obtener_token(self, username, password):
        response = self.client.post(reverse('token_obtain_pair'), {'username': username, 'password': password})
        return response.data['access']

    def test_401_sin_token(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_201_crear_estado_calculado_regla(self):
        token = self.obtener_token('normal', '123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {"producto": "Mouse", "stock_actual": 2, "ventas_esperadas": 10, "estado": "Optimo"} # Estado ignorado
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['estado'], decidir(2, 10))
        self.assertEqual(response.data['estado'], 'Critico') # Calculado por decidir(), ignora el enviado

    def test_400_datos_invalidos(self):
        token = self.obtener_token('admin', '123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        data = {"producto": "Cable", "stock_actual": -5, "ventas_esperadas": 10}
        response = self.client.post(self.url_list, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_403_viewer_no_puede_crear(self):
        token = self.obtener_token('viewer', '123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(self.url_list, {"producto": "Monitor", "stock_actual": 10, "ventas_esperadas": 5})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_403_normal_no_puede_borrar(self):
        token = self.obtener_token('normal', '123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_204_admin_borrado_logico(self):
        token = self.obtener_token('admin', '123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.registro.refresh_from_db()
        self.assertTrue(self.registro.eliminado)

    def test_patch_recalcula_estado(self):
        token = self.obtener_token('admin', '123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        # Original: stock 10, ventas 5 (Optimo). Con ventas 15: 10 >= 7.5 -> Alerta
        response = self.client.patch(self.url_detail, {"ventas_esperadas": 15})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estado'], decidir(10, 15))
        self.assertEqual(response.data['estado'], 'Alerta')

    def test_filtro_y_paginacion(self):
        token = self.obtener_token('viewer', '123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url_list + "?estado=Optimo")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data) # Prueba de paginación
        self.assertEqual(response.data['count'], 1)

    def test_404_no_encontrado(self):
        token = self.obtener_token('admin', '123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(reverse('registro-detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detalle', response.data)

    def test_html_es2_funciona(self):
        # La ruta original HTML
        response = self.client.get(reverse('lista'))
        # 302 redirige a login si requiere login, o 200 si no. Lo importante es que la ruta exista y no de 404 ni 500.
        self.assertIn(response.status_code, [200, 302])
    def test_filtro_estado_invalido_400(self):
        token = self.obtener_token('viewer', '123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(self.url_list + "?estado=Nada")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sin_token_401(self):
        self.assertEqual(self.client.get(self.url_list).status_code, status.HTTP_401_UNAUTHORIZED)

    def test_viewer_no_crea_403_y_normal_no_edita_403(self):
        token = self.obtener_token('viewer', '123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        datos = {"producto": "X", "stock_actual": 1, "ventas_esperadas": 1}
        self.assertEqual(self.client.post(self.url_list, datos, format="json").status_code, status.HTTP_403_FORBIDDEN)
        token = self.obtener_token('normal', '123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(self.client.patch(self.url_detail, {"stock_actual": 1}, format="json").status_code, status.HTTP_403_FORBIDDEN)

    def test_404_con_mensaje_claro_y_options_permitido(self):
        token = self.obtener_token('viewer', '123')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        r = self.client.get(self.url_list + "9999/")
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", r.data)
        self.assertEqual(self.client.options(self.url_list).status_code, status.HTTP_200_OK)

    def test_pantallas_html_de_la_es2_siguen_vivas(self):
        from django.test import Client
        c = Client()
        self.assertEqual(c.get("/login/").status_code, 200)
        self.assertEqual(c.get("/").status_code, 302)
        c.login(username="admin", password="123")
        self.assertEqual(c.get("/").status_code, 200)
        self.assertEqual(c.get(f"/{self.registro.pk}/editar/").status_code, 200)
