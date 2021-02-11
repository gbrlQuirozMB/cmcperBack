from preregistro.models import Medico
from rest_framework import fields, serializers


class ExtranjeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'isExtranjero', 'nacionalidad']
