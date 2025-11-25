from django import forms
from .models import Mascota

class MascotaForm(forms.ModelForm):
    """
    Formulario basado en el modelo Mascota para agregar y editar.
    """
    class Meta:
        model = Mascota
        # Campos que el refugio debe poder editar/agregar
        fields = [
            'nombre', 
            'raza', 
            'edad', 
            'tipo', 
            'genero', 
            'descripcion', 
            'foto', 
            'status', 
            'vacunado', 
            'esterilizado'
        ]
        # Opcional: Personalizar etiquetas
        labels = {
            'nombre': 'Nombre de la Mascota',
            'raza': 'Raza',
            'edad': 'Edad (en años)',
            'tipo': 'Especie',
            'status': 'Estado de Adopción',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }