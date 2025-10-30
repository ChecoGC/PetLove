from rest_framework import serializers
from .models import Mascota, SolicitudAdopcion, Mensaje, Refugio

class RefugioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refugio
        fields = '__all__'

class MascotaSerializer(serializers.ModelSerializer):
    refugio = RefugioSerializer(read_only=True)
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

