from django.shortcuts import render, get_object_or_404
from .models import Mascota


#Vista basada en una funcion
def index(request):
    template_name = "index.html"
    mascotas = Mascota.objects.all()
    context = {'mascotas': mascotas}
    return render(request, template_name,context)

def detalle_mascota(request, id):
    mascota = get_object_or_404(Mascota, id=id)
    return render(request, 'detalle.html', {'mascota': mascota})