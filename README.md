# API RESTful Inventario Logístico (ES3)

Programación Back End (TI3V41) · INACAP. El proyecto de la ES2 sigue funcionando en `/` (pantallas HTML) y ahora también expone una API RESTful bajo `/api/`, sobre el mismo modelo `Registro`, la misma regla `solucion.decidir` y la misma base de datos.

## Instalación y ejecución local
1. Crear y activar entorno virtual: `python3 -m venv venv && source venv/bin/activate`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar variables: `cp .env.example .env` y llenar `SECRET_KEY` y las claves `PASS_ADMIN`, `PASS_NORMAL`, `PASS_VIEWER`.
4. Entrar a la carpeta del proyecto: `cd miproyecto`
5. Migrar la base de datos: `python manage.py migrate`
6. Crear roles y usuarios base: `python manage.py crear_roles` (crea `admin_api`, `normal_api` y `viewer_api` con las claves del `.env`; sin clave en el `.env` no crea el usuario)
7. Correr pruebas automatizadas: `python manage.py test core`
8. Levantar el servidor: `python manage.py runserver`

* Pantallas HTML (ES2): http://127.0.0.1:8000/ (login en `/login/`)
* API: http://127.0.0.1:8000/api/registros/
* Documentación Swagger: http://127.0.0.1:8000/api/docs/

## Tabla de roles (`PermisosES2`)
| Grupo | Autenticación web (ES2) | Permisos API (ES3) |
|---|---|---|
| **admin** | Acceso total | GET, POST, PUT, PATCH, DELETE |
| **normal** | Solo lectura y creación | GET, POST |
| **viewer** | Solo lectura | GET |

## Endpoints de la API
| Verbo | Endpoint | Descripción | Código de éxito | Errores posibles |
|---|---|---|---|---|
| POST | `/api/token/` | Obtiene JWT access/refresh | 200 | 401 |
| POST | `/api/token/refresh/` | Renueva el access con el refresh | 200 | 401 |
| GET | `/api/registros/` | Lista paginada (10 por página). Filtro: `?estado=Critico` | 200 | 400, 401 |
| POST | `/api/registros/` | Crea registro; el estado lo calcula `decidir` | 201 | 400, 401, 403 |
| GET | `/api/registros/{id}/` | Detalle del registro | 200 | 401, 404 |
| PUT / PATCH | `/api/registros/{id}/` | Actualiza y recalcula el estado | 200 | 400, 401, 403, 404 |
| DELETE | `/api/registros/{id}/` | Borrado lógico (solo admin) | 204 | 401, 403, 404 |

**Ejemplo de uso del token (cURL):**
```bash
curl -i -X POST -H "Content-Type: application/json" \
  -d '{"username":"admin_api","password":"TU_CLAVE"}' http://127.0.0.1:8000/api/token/
# respuesta: {"refresh":"eyJhbGci...(truncado)","access":"eyJhbGci...(truncado)"}

curl -i -H "Authorization: Bearer eyJhbGci...(truncado)" http://127.0.0.1:8000/api/registros/
```

## Justificación de la configuración
* **JWT (simplejwt) en vez de token básico:** el access token expira a los 60 minutos y se renueva con el refresh (1 día); el token básico no caduca nunca.
* **`IsAuthenticated` global:** todo endpoint nuevo nace cerrado. `PermisosES2` reutiliza `tiene_rol` de la ES2, así los permisos de la API y de las pantallas son los mismos.
* **`PageNumberPagination`, `PAGE_SIZE = 10`:** evita devolver toda la tabla de una vez y estandariza el consumo.
* **`DefaultRouter` + `ModelViewSet`:** rutas RESTful (sustantivo en plural + verbo HTTP) sin escribirlas a mano; una sola forma de vista en toda la API.
* **Serializer con campos enumerados:** `estado` y `fecha_consulta` son de solo lectura; el estado siempre lo decide `solucion.decidir`, al crear y al editar.
* **Credenciales fuera del código:** `SECRET_KEY` y las claves de los usuarios base se leen del `.env` (no versionado), sin valores por defecto.

## Pruebas
* `python manage.py test core`: 15 pruebas automáticas (autenticación, roles, validación, paginación, filtro, borrado lógico y pantallas HTML de la ES2).
* `pruebas/evidencia_pruebas.txt`: salidas de curl con los códigos 200, 201, 204, 400, 401, 403 y 404, con los tokens truncados. Se regenera con `bash pruebas/ejecutar_pruebas.sh` (ver instrucciones dentro del script).

## Uso de IA
Ver `ia.md`.
