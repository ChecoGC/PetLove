from django.contrib import admin

from .models import Mascota, SolicitudAdopcion, Contacto

admin.site.register(Mascota)
admin.site.register(SolicitudAdopcion)
admin.site.register(Contacto)