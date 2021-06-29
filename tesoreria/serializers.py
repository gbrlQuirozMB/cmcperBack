from rest_framework import fields, serializers
from .models import *
from preregistro.models import Medico
from convocatoria.models import Convocatoria, ConvocatoriaEnrolado
from catalogos.models import CatPagos


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'


class PagosListSerializer(serializers.ModelSerializer):
    estatus = serializers.CharField(source='get_estatus_display')

    class Meta:
        model = Pago
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        if instance.medico != None:
            repr['medicoNombreApPaterno'] = instance.medico.nombre + ' ' + instance.medico.apPaterno
        else:
            repr['medicoNombreApPaterno'] = None
        if instance.institucion != None:
            repr['institucionNombre'] = instance.institucion.nombreInstitucion
        else:
            repr['institucionNombre'] = None
            
        try:
            dato = CatPagos.objects.get(id=instance.tipo)
            repr['descripcion'] = dato.descripcion
        except:
            repr['descripcion'] = 'No hay descripcion'
            
        return repr


class PagoAceptarRechazarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['id', 'estatus']
