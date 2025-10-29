from django.urls import path, include
from .views import index, mensaje
from . import views

from rest_framework import routers
from .views import MascotaViewSet , SolicitudAdopcionViewSet, MensajeViewSet

router = routers.DefaultRouter()
router.register(r'api/mascotas', MascotaViewSet)
router.register(r'api/formularios', SolicitudAdopcionViewSet)
router.register(r'api/mensaje', MensajeViewSet)

urlpatterns = [
    path('', index, name='inicio'),
    path('mascota/<int:id>/', views.detalle_mascota, name='detalle_mascota'),
    path("adoptar/<int:mascota_id>/", views.formulario_adopcion, name="formulario_adopcion"),
    path('mensaje/', mensaje, name='mensaje'),
    path('', include(router.urls)),
    path('filtrar/', views.filtrar_mascotas_view, name='filtrar_mascotas'),
]