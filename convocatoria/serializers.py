from preregistro.models import Medico
from rest_framework import fields, serializers


class EsExtranjeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'isExtranjero', 'nacionalidad']

class EstudioExtranjeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'estudioExtranjero', 'escuelaExtranjero']