from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import User, Group
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

@receiver(m2m_changed, sender=User.groups.through)
def set_staff_status_on_group_change(sender, instance, action, **kwargs):
    """
    Activa is_staff=True si el usuario es agregado al grupo 'refugio'.
    """
    if action in ['post_add', 'post_remove', 'post_clear']:
        try:
            refugio_group = Group.objects.get(name='refugio')
            is_refugio = instance.groups.filter(pk=refugio_group.pk).exists()
            
            if is_refugio and not instance.is_staff:
                instance.is_staff = True
                instance.save()
            
            elif not is_refugio and instance.is_staff and not instance.is_superuser:
                instance.is_staff = False
                instance.save()
                
        except Group.DoesNotExist:
            pass

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
    foto = models.ImageField(upload_to='media/mascotas/', blank=True, null=True)
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='disponible'
    )
    refugio = models.ForeignKey(
        'Refugio', 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='mascotas', 
        help_text="Refugio donde se encuentra la mascota."
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    vacunado = models.BooleanField(default=False)
    esterilizado = models.BooleanField(default=False)
    raza = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) - {self.status}"

    

class SolicitudAdopcion(models.Model):
    # relacionn con la mascota adoptada
    mascota = models.ForeignKey('Mascota', on_delete=models.CASCADE)

    # Datos personales
    nombre_apellido = models.CharField(max_length=100) #
    ocupacion = models.CharField(max_length=100) #
    edad = models.PositiveIntegerField() #
    telefono = models.CharField(max_length=20) #
    email = models.EmailField(blank=True, null=True) #
    facebook = models.CharField(max_length=100, blank=True, null=True) #
    instagram = models.CharField(max_length=100, blank=True, null=True) #
    direccion = models.CharField(max_length=200) #

    # Motivaciones
    motivo_general = models.TextField() #
    motivo_especifico = models.TextField() #
    persona_ideal = models.TextField() # 

    # Informacion adicional
    otros_animales = models.TextField(blank=True, null=True) #
    animales_anteriores = models.TextField(blank=True, null=True) #
    que_paso = models.TextField(blank=True, null=True) #
    familia_de_acuerdo = models.BooleanField(default=False) #
    hay_ninios = models.BooleanField(default=False) #
    edades_ninios = models.CharField(max_length=100, blank=True, null=True) #
    ninios_convivencia = models.BooleanField(default=False)  #
    alergias = models.CharField(max_length=200, blank=True, null=True) #
    tipo_vivienda = models.CharField(max_length=50, blank=True, null=True) #
    se_permiten_animales = models.BooleanField(default=False) #
    espacio_suficiente = models.BooleanField(default=False) #
    que_pasa_si_muda = models.TextField(blank=True, null=True) #
    que_pasa_si_enferma = models.TextField(blank=True, null=True) #
    tiene_veterinario = models.BooleanField(default=False) #
    donde_duerme = models.TextField(blank=True, null=True) #
    tiempo_solo_dia = models.TextField(blank=True, null = True) #
    paseos = models.TextField(blank=True, null = True) #
    responsable_gastos = models.CharField(max_length=100, blank=True, null=True) #
    situacion_empleo = models.CharField(max_length=100, blank=True, null=True)#
    puede_cubrir_gastos = models.BooleanField(default=False)

    #Cuidados y Compromiso 
    veterinario = models.BooleanField(default=False) #
    paseo = models.BooleanField(default=False) #
    plato_limpio = models.BooleanField(default=False) #
    vacunacion_desparasitacion = models.BooleanField(default=False) #
    Tiempo_juego_afecto = models.BooleanField(default=False) #

    comentarios_extra = models.TextField(blank=True, null=True) #
    fecha_solicitud = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Solicitud de {self.nombre_apellido} para {self.mascota.nombre}"

class Mensaje(models.Model):
    nombre_apellido  = models.CharField(max_length=100)
    telefono = models.CharField(max_length=12)
    email = models.EmailField()
    mensaje = models.TextField(blank=True, null=True)
    fecha_mensaje = models.DateTimeField(default=timezone.now)    
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mensajes"
    )

    def __str__(self):
        return f"mensaje de {self.nombre_apellido} del {self.fecha_mensaje}" 
    

class Refugio(models.Model):
    refugio_id = models.AutoField(primary_key=True) 
    
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, help_text="Calle, número, colonia, etc.")
    estado = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(blank=True, null=True)
    capacidad = models.PositiveIntegerField(
        help_text="Número máximo de animales que puede albergar",
        default=0
    )

    def __str__(self):
        return self.nombre
    

    
def is_refugio(self):
    return self.groups.filter(name='refugio').exists()

User.add_to_class('is_refugio', is_refugio)

class PerfilRefugio(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_refugio' 
    )
    refugio = models.ForeignKey(
        'Refugio',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='usuarios'
    )

    def __str__(self):
        return f"Perfil de {self.usuario.username}"