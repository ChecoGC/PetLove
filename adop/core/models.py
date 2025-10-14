from django.db import models
from django.utils import timezone




from django.db import models

class Mascota(models.Model):
    STATUS_CHOICES = [
        ('disponible', 'Disponible'),
        ('adoptado', 'Adoptado'),
        ('en_proceso', 'En proceso de adopción'),
    ]

    GENERO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
        ('desconocido', 'Desconocido'),
    ]

    TIPO_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    raza = models.CharField(max_length=100, blank=True, null=True)
    edad = models.PositiveIntegerField(
        help_text="Edad aproximada en años",
        default=0
    )
    tipo = models.CharField(
        max_length=30,
        choices=TIPO_CHOICES,
        default='otro'
    )
    genero = models.CharField(
        max_length=20,
        choices=GENERO_CHOICES,
        default='desconocido'
    )
    descripcion = models.TextField(blank=True)
    foto = models.ImageField(upload_to='mascotas/', blank=True, null=True)
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='disponible'
    )

    fecha_registro = models.DateTimeField(auto_now_add=True)
    vacunado = models.BooleanField(default=False)
    esterilizado = models.BooleanField(default=False)
    raza = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) - {self.status}"

""" EL modelo Mascota esta muy escueto, agregar:
    status
    raza
    edad
    tipo de animal(perro, gato, etc)
    genero
    agrega otros si crees que son necesarios

class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="mascotas",null=True, blank=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre
    """
    

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