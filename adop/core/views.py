import requests
from django.shortcuts import render, get_object_or_404
from .models import Mascota, SolicitudAdopcion, Mensaje, Refugio

from rest_framework import viewsets
from .serializers import MascotaSerializer, SolicitudAdopcionSerializer, MensajeSerializer, RefugioSerializer
from .models import Mascota

from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from .models import Mascota, Refugio

#Vista basada en una funcion
# cargan los datos desde la api

def index(request):
    # template_name = "index.html"
    # mascotas = Mascota.objects.all()
    # context = {'mascotas': mascotas}
    # return render(request, template_name)
    api_url = request.build_absolute_uri('/api/mascotas/')
    response = requests.get(api_url)

    if response.status_code == 200:
        mascotas = response.json()
    else:
        mascotas = []

    context = {'mascotas': mascotas}
    return render(request, 'index.html', context)


def detalle_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    return render(request, 'detalle.html', {"mascota": mascota})

class MascotaViewSet(viewsets.ModelViewSet):
    queryset = Mascota.objects.all()
    serializer_class = MascotaSerializer

def formulario_adopcion(request, mascota_id):
    mascota = Mascota.objects.get(id=mascota_id)
    return render(request, "formulario_adopcion.html", {"mascota": mascota})

class RefugioViewSet(viewsets.ModelViewSet):
    queryset = Refugio.objects.all()
    serializer_class = RefugioSerializer

class SolicitudAdopcionViewSet(viewsets.ModelViewSet):
    queryset = SolicitudAdopcion.objects.all()
    serializer_class = SolicitudAdopcionSerializer

class MensajeViewSet(viewsets.ModelViewSet):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer

def mensaje(request):
    template_name = 'contacto.html'
    return render (request, template_name)

def registrar_refugio(request):
    template_name = 'registro_refugio.html'
    return render(request, template_name)

def filtrar_mascotas_view(request):
    especie = request.GET.get('especie', '')
    estado = request.GET.get('estado', '')
    municipio = request.GET.get('municipio', '') 

    mascotas = Mascota.objects.all().select_related('refugio')

    if especie:
        mascotas = mascotas.filter(tipo__iexact=especie)
    if estado:
        mascotas = mascotas.filter(refugio__estado__iexact=estado)
    if municipio:
        mascotas = mascotas.filter(refugio__municipio__iexact=municipio)

    data = []
    for m in mascotas:
        data.append({
            'id': m.id,
            'nombre': m.nombre,
            'descripcion': m.descripcion,
            'foto': request.build_absolute_uri(m.foto.url) if m.foto else '',
            'tipo': m.tipo,
            'estado': m.refugio.estado if m.refugio else '',
            'municipio': m.refugio.municipio if m.refugio else '',
            'status': m.status
        })

    return JsonResponse({'mascotas': data})



def obtener_filtros_ubicacion(request):
    estado = request.GET.get('estado', None)
    estados = Refugio.objects.values_list('estado', flat=True).distinct().order_by('estado')

    if estado:
        municipios = Refugio.objects.filter(estado=estado).values_list('municipio', flat=True).distinct().order_by('municipio')
    else:
        municipios = Refugio.objects.values_list('municipio', flat=True).distinct().order_by('municipio')

    return JsonResponse({
        'estados': list(estados),
        'municipios': list(municipios)
    })