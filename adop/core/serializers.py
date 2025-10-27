from rest_framework import serializers
from .models import Mascota, SolicitudAdopcion, Mensaje

class MascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mascota
        fields = '__all__'

class SolicitudAdopcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudAdopcion
        fields = '__all__'

class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = '__all__'