from django.urls import path, include
from .views import index, mensaje, registrar_refugio
from . import views

from rest_framework import routers
from .views import MascotaViewSet , SolicitudAdopcionViewSet, MensajeViewSet, RefugioViewSet

router = routers.DefaultRouter()
router.register(r'api/mascotas', MascotaViewSet)
router.register(r'api/formularios', SolicitudAdopcionViewSet)
router.register(r'api/mensaje', MensajeViewSet)
router.register(r'api/refugios', RefugioViewSet)


urlpatterns = [
    path('', index, name='inicio'),
    path('mascota/<int:id>/', views.detalle_mascota, name='detalle_mascota'),
    path("adoptar/<int:mascota_id>/", views.formulario_adopcion, name="formulario_adopcion"),
    path('mensaje/', mensaje, name='mensaje'),
    path('api/filtros-ubicacion/', views.obtener_filtros_ubicacion, name='filtros_ubicacion_api'),
    path('registrar-refugio/', registrar_refugio, name='registrar_refugio'),
    path('', include(router.urls)),
    path('filtrar/', views.filtrar_mascotas_view, name='filtrar_mascotas'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
