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
    """
    Devuelve listas únicas de estados y municipios de los refugios.
    Si se recibe 'estado', solo devuelve los municipios de ese estado.
    """
    
    # 1. Obtener el parámetro 'estado' de la petición GET (si existe)
    estado_seleccionado = request.GET.get('estado', None)

    # 2. Obtener la lista completa de estados (siempre se necesita para el combo principal)
    estados_unicos = Refugio.objects.values_list('estado', flat=True).distinct().order_by('estado')
    
    # 3. Definir el QuerySet base para municipios
    municipios_qs = Refugio.objects
    
    # 4. APLICAR EL FILTRO DE CASCADA: Si se seleccionó un estado, filtramos los municipios
    if estado_seleccionado:
        # Filtra los municipios solo para el estado seleccionado
        municipios_unicos = municipios_qs.filter(estado=estado_seleccionado).values_list('municipio', flat=True).distinct().order_by('municipio')
    else:
        # Si no se seleccionó estado, devuelve todos los municipios (como se hacía antes)
        municipios_unicos = municipios_qs.values_list('municipio', flat=True).distinct().order_by('municipio')
        
    data = {
        'estados': list(estados_unicos),
        'municipios': list(municipios_unicos)
    }
    
    return JsonResponse(data)