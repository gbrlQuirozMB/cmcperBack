from rest_framework import fields, serializers
from .models import *
from preregistro.models import Medico
from convocatoria.models import *
from certificados.models import Certificado


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


class MedResidenteExtrasDetailView(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnrolado
        fields = ['catSedes', 'catTiposExamen']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['catTiposExamen'] = instance.catTiposExamen.descripcion
        repr['catSedes'] = instance.catSedes.descripcion

        return repr


class MedCertificadoListSerializer(serializers.ModelSerializer):
    sexo = serializers.CharField(source='get_sexo_display', read_only=True)

    class Meta:
        model = Medico
        fields = ['id', 'numRegistro', 'telConsultorio', 'telParticular', 'telCelular', 'email', 'sexo']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['nombreCompleto'] = instance.nombre + ' ' + instance.apPaterno + ' ' + instance.apMaterno
        try:
            dato = Certificado.objects.filter(medico=instance.id)[0]
            repr['estatusVigencia'] = dato.get_estatus_display()
        except:
            repr['estatusVigencia'] = 'No existe'

        return repr


class MedCertificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'


class MedCertificadoFechasSerializer(serializers.ModelSerializer):
    estatus = serializers.CharField(source='get_estatus_display')

    class Meta:
        model = Certificado
        fields = ['fechaCertificacion', 'fechaCaducidad', 'estatus']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['nombre'] = instance.medico.nombre + ' ' + instance.medico.apPaterno
        repr['numRegistro'] = instance.medico.numRegistro
        anio = int(instance.fechaCaducidad.strftime('%Y'))
        repr['anioProxima'] = anio

        return repr
