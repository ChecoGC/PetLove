from django.shortcuts import render, get_object_or_404
from .models import Mascota, SolicitudAdopcion, Mensaje

from rest_framework import viewsets
from .serializers import MascotaSerializer, SolicitudAdopcionSerializer, MensajeSerializer

#Vista basada en una funcion
def index(request):
    template_name = "index.html"
    mascotas = Mascota.objects.all()
    context = {'mascotas': mascotas}
    return render(request, template_name,context)

def detalle_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    return render(request, 'detalle.html', {"mascota": mascota})

class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer

def formulario_adopcion(request, mascota_id):
    mascota = Mascota.objects.get(id=mascota_id)
    return render(request, "formulario_adopcion.html", {"mascota": mascota})

class SolicitudAdopcionViewSet(viewsets.ModelViewSet):
    queryset = SolicitudAdopcion.objects.all()
    serializer_class = SolicitudAdopcionSerializer

class MensajeViewSet(viewsets.ModelViewSet):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer
def mensaje(request):
    template_name = 'contacto.html'
    return render (request, template_name)

def filtrar_mascotas_view(request):
    especie = request.GET.get('especie', '')

    if especie:
        mascotas = Mascota.objects.filter(tipo__iexact=especie)
    else:
        mascotas = Mascota.objects.all()
    context = {'mascotas': mascotas}
    return render(request, 'mascota_list.html', context)