from rest_framework import fields, serializers
from .models import *
from preregistro.models import Medico


class MedResidenteListSerializer(serializers.ModelSerializer):
    sexo = serializers.CharField(source='get_sexo_display', read_only=True)

    class Meta:
        model = Medico
        fields = ['id', 'telConsultorio', 'telParticular', 'telJefEnse', 'email', 'sexo']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['nombreCompleto'] = instance.nombre + ' ' + instance.apPaterno + ' ' + instance.apMaterno

        return repr


class MedResidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'
