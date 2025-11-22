from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Mascota, SolicitudAdopcion, Mensaje, Refugio, PerfilRefugio


class PerfilRefugioInline(admin.StackedInline):
    model = PerfilRefugio
    can_delete = False
    verbose_name_plural = 'Perfil de Refugio'
    fk_name = 'usuario'

class UsuarioRefugioAdmin(BaseUserAdmin):
    inlines = (PerfilRefugioInline,)

admin.site.unregister(User)
admin.site.register(User, UsuarioRefugioAdmin)
admin.site.register(Refugio)
admin.site.register(Mensaje)


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'status', 'refugio')
    list_filter = ('status', 'tipo', 'refugio')
    search_fields = ('nombre', 'raza')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if not request.user.groups.filter(name='refugio').exists() and request.user.is_superuser:
             return qs
        if not request.user.groups.filter(name='refugio').exists():
            return qs

        try:
            refugio = request.user.perfil_refugio.refugio
            if refugio:
                return qs.filter(refugio=refugio)
            else:
                return qs.none() 
        except PerfilRefugio.DoesNotExist:
            return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "refugio" and request.user.groups.filter(name='refugio').exists():
            try:
                refugio_usuario = request.user.perfil_refugio.refugio
                kwargs["queryset"] = Refugio.objects.filter(pk=refugio_usuario.pk)
            except (PerfilRefugio.DoesNotExist, AttributeError):
                kwargs["queryset"] = Refugio.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name='refugio').exists() and not change:
            try:
                obj.refugio = request.user.perfil_refugio.refugio
            except PerfilRefugio.DoesNotExist:
                pass 
        super().save_model(request, obj, form, change)

@admin.register(SolicitudAdopcion)
class SolicitudAdopcionAdmin(admin.ModelAdmin):
    list_display = ('nombre_apellido', 'mascota', 'fecha_solicitud')
    list_filter = ('mascota__refugio',)
    search_fields = ('nombre_apellido', 'mascota__nombre')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        if not request.user.groups.filter(name='refugio').exists() and request.user.is_superuser:
             return qs
        if not request.user.groups.filter(name='refugio').exists():
            return qs

        try:
            refugio = request.user.perfil_refugio.refugio
            if refugio:
                return qs.filter(mascota__refugio=refugio)
            else:
                return qs.none()
        except PerfilRefugio.DoesNotExist:
            return qs.none()