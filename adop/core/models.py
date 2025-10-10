from django.db import models

class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to="mascotas",null=True, blank=True)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre