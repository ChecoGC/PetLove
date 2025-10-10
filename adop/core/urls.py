from django.urls import path
from .views import index
from . import views


urlpatterns = [
    path('', index),
    path('mascota/<int:id>/', views.detalle_mascota, name='detalle_mascota'),
]
