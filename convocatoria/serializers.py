from preregistro.models import Medico
from .models import *
from rest_framework import serializers
from api.logger import log
from api.exceptions import *


class EsExtranjeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'isExtranjero', 'nacionalidad']


class EstudioExtranjeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'estudioExtranjero', 'escuelaExtranjero']


class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = ['catSedes']


class TipoExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoExamen
        fields = ['catTiposExamen']


class ConvocatoriaSerializer(serializers.ModelSerializer):
    sedes = SedeSerializer(required=False, many=True)
    tiposExamen = TipoExamenSerializer(required=False, many=True)

    class Meta:
        model = Convocatoria
        # evito poner todo el listado de campos
        fields = [f.name for f in model._meta.fields] + ['sedes'] + ['tiposExamen']

    def create(self, validated_data):
        sedesData = validated_data.pop('sedes')
        for dato in sedesData:
            if not bool(dato):
                log.info(f'campos incorrectos: catSedes')
                raise CamposIncorrectos({"catSedes": ["Este campo es requerido"]})

        tiposExameneData = validated_data.pop('tiposExamen')
        for dato in tiposExameneData:
            if not bool(dato):
                log.info(f'campos incorrectos: catTiposExamen')
                raise CamposIncorrectos({"catTiposExamen": ["Este campo es requerido"]})

        convocatoria = Convocatoria.objects.create(**validated_data)
        for sedeData in sedesData:
            Sede.objects.create(**sedeData, convocatoria=convocatoria)
        for tipoExamenData in tiposExameneData:
            TipoExamen.objects.create(**tipoExamenData, convocatoria=convocatoria)
        # return validated_data # incompleto porque ya se le quito la llave 'sedes'
        return convocatoria


class ConvocatoriaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convocatoria
        fields = ['id', 'nombre']


class CatSedesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatSedes
        fields = '__all__'


class SedeGetDetailSerializer(serializers.ModelSerializer):
    catSedes = CatSedesSerializer(read_only=True)

    class Meta:
        model = Sede
        fields = ['catSedes']


class CatTiposExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatTiposExamen
        fields = '__all__'


class TiposExamenGetDetailSerializer(serializers.ModelSerializer):
    catTiposExamen = CatTiposExamenSerializer(read_only=True)

    class Meta:
        model = TipoExamen
        fields = ['catTiposExamen']


class ConvocatoriaGetDetailSerializer(serializers.ModelSerializer):
    sedes = SedeGetDetailSerializer(read_only=True, many=True)
    tiposExamen = TiposExamenGetDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Convocatoria
        fields = [f.name for f in model._meta.fields] + ['sedes'] + ['tiposExamen']


class ConvocatoriaArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convocatoria
        fields = ['id', 'archivo']


class ConvocatoriaBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convocatoria
        fields = ['id', 'banner']


class ConvocatoriaEnroladoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnrolado
        fields = '__all__'


class ConvocatoriaEnroladoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnroladoDocumento
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        dato = CatTiposDocumento.objects.get(id=instance.catTiposDocumento.id)
        repr['tipoDocumento'] = dato.descripcion
        return repr


class ConvocatoriaEnroladoDocumentoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnroladoDocumento
        fields = ['id', 'documento', 'isValidado', 'rechazoValidado', 'notasValidado']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        dato = CatTiposDocumento.objects.get(id=instance.catTiposDocumento.id)
        repr['tipoDocumento'] = dato.descripcion
        return repr


class ConvocatoriaDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnroladoDocumento
        fields = ['id', 'documento']
