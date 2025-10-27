from django.contrib import admin

from .models import Mascota, SolicitudAdopcion, Mensaje

admin.site.register(Mascota)
admin.site.register(SolicitudAdopcion)
admin.site.register(Mensaje)