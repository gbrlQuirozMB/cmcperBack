from preregistro.models import Medico
from .models import *
from rest_framework import fields, serializers
from api.logger import log
from api.exceptions import *

import datetime

class CertificadoDatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['nombre'] = instance.medico.nombre + ' ' + instance.medico.apPaterno
        repr['numRegistro'] = instance.medico.numRegistro
        proximaCertificacion = instance.anioCertificacion + 5
        repr['proximaCertificacion'] = proximaCertificacion
        anio = int(datetime.datetime.now().strftime('%Y'))
        # anio = 2004 # para probar la vigencia
        repr['estatus'] = 'vigente'
        if (proximaCertificacion - anio) == 1:
            repr['estatus'] = 'esta por vencer'
        if (proximaCertificacion - anio) < 1:
            repr['estatus'] = 'vencido'
        return repr
