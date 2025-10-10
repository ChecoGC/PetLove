from django.urls import path
from .views import index
from . import views


urlpatterns = [
    path('', index),
    path('mascota/<int:id>/', views.detalle_mascota, name='detalle_mascota'),
    path("adoptar/<int:mascota_id>/", views.formulario_adopcion, name="formulario_adopcion"),
]
