from django.shortcuts import render, get_object_or_404
from .models import Mascota, SolicitudAdopcion, Mensaje, Refugio

from rest_framework import viewsets
from .serializers import MascotaSerializer, SolicitudAdopcionSerializer, MensajeSerializer, RefugioSerializer
from django.shortcuts import render
from .models import Mascota
from django.http import JsonResponse

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
        
    context = {'mascotas': mascotas}
    return render(request, 'mascota_list.html', context)



def obtener_filtros_ubicacion(request):
    """Devuelve listas únicas de estados y municipios de los refugios."""
    
    estados_unicos = Refugio.objects.values_list('estado', flat=True).distinct().order_by('estado')
    
    municipios_unicos = Refugio.objects.values_list('municipio', flat=True).distinct().order_by('municipio')
    
    data = {
        'estados': list(estados_unicos),
        'municipios': list(municipios_unicos)
    }
    
    return JsonResponse(data)