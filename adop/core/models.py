from django.db import models
from django.utils import timezone

class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="mascotas",null=True, blank=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class SolicitudAdopcion(models.Model):
    # relacionn con la mascota adoptada
    mascota = models.ForeignKey('Mascota', on_delete=models.CASCADE)

    # Datos personales
    nombre_apellido = models.CharField(max_length=100)
    ocupacion = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    correo = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=200)

    # Motivaciones
    motivo_general = models.TextField()
    motivo_especifico = models.TextField()

    # Informacion adicional
    otros_animales = models.TextField(blank=True, null=True)
    historial_animales = models.TextField(blank=True, null=True)
    acuerdo_familia = models.BooleanField(default=False)
    hay_ninios = models.BooleanField(default=False)
    edades_ninios = models.CharField(max_length=100, blank=True, null=True)
    alergias = models.CharField(max_length=200, blank=True, null=True)
    tipo_vivienda = models.CharField(max_length=50, blank=True, null=True)
    se_permiten_animales = models.BooleanField(default=False)
    espacio_suficiente = models.BooleanField(default=False)
    que_pasa_si_muda = models.TextField(blank=True, null=True)
    cambios_trato = models.TextField(blank=True, null=True)
    situacion_empleo = models.CharField(max_length=100, blank=True, null=True)
    responsable_gastos = models.CharField(max_length=100, blank=True, null=True)
    puede_cubrir_gastos = models.BooleanField(default=False)
    cuidados = models.TextField(blank=True, null=True)
    veterinario = models.CharField(max_length=100, blank=True, null=True)
    comentarios_extra = models.TextField(blank=True, null=True)

    fecha_solicitud = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Solicitud de {self.nombre_apellido} para {self.mascota.nombre}"