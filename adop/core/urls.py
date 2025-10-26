from django.urls import path, include
from .views import index, contacto
from . import views

from rest_framework import routers
from .views import MascotaViewSet , SolicitudAdopcionViewSet, ContactoViewSet

router = routers.DefaultRouter()
router.register(r'api/mascotas', MascotaViewSet)
router.register(r'api/formularios', SolicitudAdopcionViewSet)
router.register(r'api/contacto', ContactoViewSet)

urlpatterns = [
    path('', index, name='inicio'),
    path('mascota/<int:id>/', views.detalle_mascota, name='detalle_mascota'),
    path("adoptar/<int:mascota_id>/", views.formulario_adopcion, name="formulario_adopcion"),
    path('contacto/', contacto, name='contacto'),
    path('', include(router.urls)),
]
