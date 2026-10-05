from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.api_views import RegistroViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core import views 

router = DefaultRouter()
router.register(r"registros", RegistroViewSet, basename="registro")

urlpatterns = [
    # --- RUTAS DE LA API RESTFUL (ES3) ---
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/", include(router.urls)),
    
    # --- RUTAS HTML ORIGINALES (ES2) ---
    path('admin/', admin.site.urls),
    path('', views.lista, name='lista'),
    path('crear/', views.crear, name='crear'),
    path('<int:pk>/editar/', views.editar, name='editar'),
    path('<int:pk>/eliminar/', views.eliminar, name='eliminar'),
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
]

# Manejador de error 404 personalizado (Requisito Extras)
handler404 = 'core.exceptions.custom_404_view'