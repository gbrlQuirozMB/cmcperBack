from rest_framework import fields, serializers
from .models import *
from certificados.models import Certificado


class MedicosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = ['id']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['nombreDiploma'] = instance.medico.diplomaConacem
        repr['numCertificado'] = instance.medico.numRegistro
        repr['medicoId'] = instance.medico.id

        return repr


class DetalleConcacemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleConcacem
        fields = ['medico']


class ConacemSerializer(serializers.ModelSerializer):
    medicos = DetalleConcacemSerializer(required=False, many=True)

    class Meta:
        model = Conacem
        fields = [f.name for f in model._meta.fields] + ['medicos']

    def create(self, validated_data):
        # *** no trae la llave 'medicos'
        if validated_data.get('medicos') is None:
            conacem = Conacem.objects.create(**validated_data)
            return conacem
        # *** si trae la llave medicos
        medicosData = validated_data.pop('medicos')
        conacem = Conacem.objects.create(**validated_data)
        # *** preparamos para asignar lugares
        hoja = validated_data.get("hoja")
        lugar = validated_data.get("lugar")
        cupo = validated_data.get("cupo")
        # *** guardamos lo id de los certificados para modificarlos mas adelante
        numerosCertificado = []
        # *** vamos a procesar uno por uno de los medicos que trae el json
        for medicoData in medicosData:
            # *** se asignan lugares
            medicoData.update({'libro': hoja})
            medicoData.update({'foja': lugar})
            # *** hay que obtener los id del certificado y ponerlo en el detalle
            numCertificado = Certificado.objects.filter(medico=medicoData['medico'].id, isConacem=False).values_list('id', flat=True).first()
            # *** guardamos lo id de los certificados para modificarlos mas adelante
            numerosCertificado.append(numCertificado)
            # *** print(f'--->>>numCertificado: {numCertificado}')
            medicoData.update({'numCertificado': numCertificado})
            # *** se crea el registro
            DetalleConcacem.objects.create(**medicoData, conacem=conacem)
            # *** se actualiza el lugar
            lugar = lugar + 1
            if lugar > cupo:
                lugar = 1
                hoja = hoja + 1
            # print(f'--->>>{medicoData["medico"].id}')
        # *** obtenemos los ids para modificar los registros de la tabla certificados y ya no se listen como medicos disponibles
        # ids = [x['medico'].id for x in medicosData]
        # Certificado.objects.filter(medico_id__in=ids).update(isConacem=True)
        # *** con los ids de los certificados sincronizamos las fechas
        Certificado.objects.filter(id__in=numerosCertificado).update(
            isConacem=True,
            fechaCertificacion=validated_data.get('fechaValidezDel'),
            fechaCaducidad=validated_data.get('fechaValidezAl'),
            estatus=1)

        return conacem


class ConacemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conacem
        fields = ['id', 'fechaEnvio', 'fechaEmision', 'fechaValidezDel', 'fechaValidezAl', 'isCompletado']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['presidente'] = instance.tituloPresidente + ' ' + instance.nombrePresidente
        repr['responsable'] = instance.tituloResponsable + ' ' + instance.nombreResponsable

        return repr


class DetalleConacemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleConcacem
        fields = ['numCertificado', 'libro', 'foja']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['diplomaConacem'] = instance.medico.diplomaConacem
        repr['lugar'] = instance.conacem.lugar

        return repr
