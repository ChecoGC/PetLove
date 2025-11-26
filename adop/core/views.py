import requests
from django.shortcuts import render, get_object_or_404, redirect
from .models import Mascota, SolicitudAdopcion, Mensaje, Refugio, PerfilRefugio
from rest_framework import viewsets, permissions
from .serializers import MascotaSerializer, SolicitudAdopcionSerializer, MensajeSerializer, RefugioSerializer
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MascotaForm
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

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            #aqui asigna el usuario
            serializer.save(usuario=self.request.user)
        else:
            serializer.save()

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

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # inicia sesion
            if user.groups.filter(name='refugio').exists():
                return redirect('inicio')
            elif user.groups.filter(name='adoptante').exists():
                return redirect('inicio')
            else:
                return redirect('inicio')
        else:
            return render(request, 'login.html', {'error': 'Usuario y/o contraseǹa incorrectas'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('inicio')

# devuelve los mensajes de el usuario
class MisMensajesViewSet(viewsets.ModelViewSet):
    serializer_class = MensajeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Mensaje.objects.all()
    def get_queryset(self):
        return Mensaje.objects.filter(usuario=self.request.user)
    

@login_required
def mis_mensajes_page(request):
    return render(request, 'mis_mensajes.html')


def editar_mensaje_page(request):
    return render(request, 'editar_mensaje.html')

@login_required
def panel_refugio(request):
    """
    Vista para el panel de administración del Refugio.
    Solo accesible para usuarios que pertenecen al grupo 'refugio'.
    """
    #Revisar que el usuario pertenece al grupo refugio
    if not request.user.is_refugio:
        # Si no pertenece, redirigir a la página de inicio o mostrar un error
        return redirect('inicio')
    
    # Obtener el refugio asociado al usuario
    try:
        perfil = request.user.perfil_refugio
        refugio = perfil.refugio
    except:
        # Si el usuario es 'refugio' pero no tiene un PerfilRefugio asociado
        refugio = None

    # Obtener las mascotas que pertenecen a este refugio
    mascotas_propias = Mascota.objects.none()
    if refugio:
        mascotas_propias = Mascota.objects.filter(refugio=refugio).order_by('-fecha_registro')

    context = {
        'refugio': refugio,
        'mascotas_propias': mascotas_propias,
        'conteo_mascotas': mascotas_propias.count(),
        
    }
    
    return render(request, 'panel_refugio.html', context)

def _get_refugio_context(user):
    """Función auxiliar para obtener el objeto Refugio del usuario."""
    try:
        return user.perfil_refugio.refugio
    except (PerfilRefugio.DoesNotExist, AttributeError):
        return None

@login_required
def agregar_mascota(request):
    if not request.user.is_refugio:
        return redirect('inicio')
    
    refugio = _get_refugio_context(request.user)
    if not refugio:
        # Manejar el caso donde el usuario 'refugio' no está vinculado a un Refugio
        return redirect('panel_refugio') 

    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.refugio = refugio # Asigna automáticamente el refugio
            mascota.save()
            return redirect('panel_refugio')
    else:
        form = MascotaForm()
        
    return render(request, 'agregar_mascota.html', {'form': form, 'refugio': refugio})


@login_required
def editar_mascota(request, mascota_id):
    if not request.user.is_refugio:
        return redirect('inicio')

    # Solo permite editar mascotas propias del refugio
    refugio = _get_refugio_context(request.user)
    mascota = get_object_or_404(Mascota, id=mascota_id, refugio=refugio)

    if request.method == 'POST':
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('panel_refugio')
    else:
        form = MascotaForm(instance=mascota)
        
    return render(request, 'editar_mascota.html', {'form': form, 'mascota': mascota})

@login_required
def eliminar_mascota(request, mascota_id):
    """
    Elimina una mascota, verificando que el usuario logueado sea el refugio propietario.
    Solo acepta peticiones POST (por seguridad CSRF).
    """
    if not request.user.is_refugio:
        return redirect('inicio')
    
    # 1. Obtener el refugio del usuario
    refugio = _get_refugio_context(request.user)
    if not refugio:
        return redirect('panel_refugio')

    # 2. Obtener la mascota y asegurar que pertenece a este refugio
    # Si la mascota no existe o no pertenece a este refugio, Django devuelve 404
    mascota = get_object_or_404(Mascota, id=mascota_id, refugio=refugio)

    if request.method == 'POST':
        mascota.delete()
        # Opcional: Podrías usar el framework de mensajes de Django aquí para mostrar una notificación de éxito.
        return redirect('panel_refugio')
        
    # Si la petición no es POST, redirigir al panel.
    return redirect('panel_refugio')