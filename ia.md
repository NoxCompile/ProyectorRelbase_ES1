# Uso Crítico de Inteligencia Artificial

### Incidente 1: Arquitectura y Enrutamiento (Criterio 3.1.4)
* **Qué pedí:** Generar el ViewSet y actualizar el archivo `urls.py` con el `DefaultRouter` para la API.
* **Qué respondió la IA:** Reescribió mi `miproyecto/urls.py` agregando `path("", include("core.urls"))`, borrando las rutas previas.
* **Qué estaba mal:** Esto rompió el proyecto con un `ModuleNotFoundError` (mi app no usaba `core.urls`). Al borrar mis rutas originales, la IA violó la regla principal de la ES3: mantener vivas y funcionales las pantallas HTML de la ES2.
* **Qué hice yo:** Rechacé el código. Extraje mi enrutamiento original de la ES2 (`views.lista`, `views.crear`, etc.) y lo unifiqué manualmente bajo las rutas de la API, logrando que ambas interfaces convivan.

### Incidente 2: Seguridad y Autenticación (Criterio 3.1.2)
* **Qué pedí:** Una configuración para probar los endpoints localmente en el navegador sin bloquearme por autenticación.
* **Qué respondió la IA:** Sugirió modificar `DEFAULT_PERMISSION_CLASSES` a `AllowAny` en `settings.py` y usar `@csrf_exempt`.
* **Qué estaba mal:** Usar `AllowAny` deja la API abierta a internet. Apagar la seguridad para probar es una pésima práctica que el criterio 3.1.2 castiga.
* **Qué hice yo:** Descarté la sugerencia. Mantuve `IsAuthenticated` global, configuré `djangorestframework-simplejwt` y creé la clase `PermisosES2` basándome en mi lógica previa (`tiene_rol`). Verifiqué todo inyectando el token por cURL.

### Incidente 3: Lógica en los Serializadores (Criterio 3.1.3)
* **Qué pedí:** Generar el serializador para el modelo `Registro`.
* **Qué respondió la IA:** Sugirió `fields = "__all__"` y omitió proteger los campos calculados.
* **Qué estaba mal:** Exponía campos de auditoría (`eliminado`, `fecha_eliminacion`) y permitía editar el campo `estado`, lo cual anula mi regla de negocio.
* **Qué hice yo:** Definí explícitamente la lista `fields`, incluí el `id` y marqué `estado` y `fecha_consulta` como `read_only_fields`.