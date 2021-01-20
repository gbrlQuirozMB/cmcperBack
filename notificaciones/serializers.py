from rest_framework import serializers

from .models import *


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'
        
        
class NotificacionLeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'
        # read_only_fields = ['leido']
        read_only_fields = [f.name for f in Notificacion._meta.get_fields()]
        