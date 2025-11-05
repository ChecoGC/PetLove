from django.urls import path, include
from .views import index, mensaje, registrar_refugio
from . import views

from rest_framework import routers
from .views import MascotaViewSet , SolicitudAdopcionViewSet, MensajeViewSet, RefugioViewSet, MisMensajesViewSet

router = routers.DefaultRouter()
router.register(r'api/mascotas', MascotaViewSet)
router.register(r'api/formularios', SolicitudAdopcionViewSet)
router.register(r'api/mensaje', MensajeViewSet)
router.register(r'api/refugios', RefugioViewSet)
router.register(r'api/mis-mensajes', MisMensajesViewSet, basename="mis-mensajes")


urlpatterns = [
    path('', index, name='inicio'),
    path('mascota/<int:id>/', views.detalle_mascota, name='detalle_mascota'),
    path("adoptar/<int:mascota_id>/", views.formulario_adopcion, name="formulario_adopcion"),
    path('mensaje/', mensaje, name='mensaje'),
    path('api/filtros-ubicacion/', views.obtener_filtros_ubicacion, name='filtros_ubicacion_api'),
    path('registrar-refugio/', registrar_refugio, name='registrar_refugio'),
    path('filtrar/', views.filtrar_mascotas_view, name='filtrar_mascotas'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('mis-mensajes/', views.mis_mensajes_page, name='mis_mensajes_page'),
    path('editar_mensaje/', views.editar_mensaje_page, name='editar_mensaje_page'),
    path('', include(router.urls)),
]
