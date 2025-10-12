from django.urls import path, include
from .views import index
from . import views

from rest_framework import routers
from .views import MascotaViewSet , SolicitudAdopcionViewSet

router = routers.DefaultRouter()
router.register(r'mascotas', MascotaViewSet)
router.register(r'formularios', SolicitudAdopcionViewSet)

urlpatterns = [
    path('', index),
    path('mascota/<int:id>/', views.detalle_mascota, name='detalle_mascota'),
    path("adoptar/<int:mascota_id>/", views.formulario_adopcion, name="formulario_adopcion"),
    path('', include(router.urls)),
]
