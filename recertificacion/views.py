from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from preregistro.models import Medico

from api.logger import log
from api.exceptions import *

from .serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status, permissions


# Create your views here.
# class CertificadoDatosDetailView(RetrieveAPIView):
#     serializer_class = CertificadoDatosSerializer
#     lookup_field = 'medico'
#     lookup_url_kwarg = 'medicoId'

#     def get_queryset(self):
#         # queryset = Certificado.objects.filter(isVencido=False)
#         # queryset = Certificado.objects.filter(estatus=1)
#         # queryset = Certificado.objects.order_by('-actualizado_en')[0]
#         queryset = Certificado.objects.filter()
#         return queryset


class CertificadoDatosDetailView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        queryset = Certificado.objects.filter(medico=medicoId)[0]
        serializer = CertificadoDatosSerializer(queryset)
        return Response(serializer.data)


class AvanceMedicoCapituloDetailView(RetrieveAPIView):
    # serializer_class = AvanceMedicoCapituloSerializer

    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        capituloId = kwargs['capituloId']
        try:
            datosCapitulo = Capitulo.objects.get(id=capituloId)
            queryset = RecertificacionItemDocumento.objects.filter(medico=medicoId, item__subcapitulo__capitulo=capituloId, estatus=1).aggregate(Sum('puntosOtorgados'))
            if queryset['puntosOtorgados__sum'] is None:
                raise ResponseError('Médico no ecnontrado', 404)
            puntosOtorgados = queryset['puntosOtorgados__sum']
            avance = round(puntosOtorgados * 100 / datosCapitulo.puntos, 2)
            avanceMedicoCapitulo = AvanceMedicoCapitulo(datosCapitulo.descripcion, datosCapitulo.puntos, puntosOtorgados, avance)
            serializer = AvanceMedicoCapituloSerializer(avanceMedicoCapitulo)
            # return Response(JSONRenderer().render(serializer.data))
            return Response(serializer.data)
        except Capitulo.DoesNotExist:
            raise ResponseError('Capítulo no encontrado', 404)


class PuntosCapituloListView(ListAPIView):
    queryset = Capitulo.objects.all()
    serializer_class = PuntosCapituloListSerializer


class PuntosCapituloDetailView(RetrieveAPIView):
    queryset = Capitulo.objects.filter()
    serializer_class = PuntosCapituloDetailSerializer


class PorcentajeGeneralMedicoDetailView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        try:
            datosMedico = Medico.objects.get(id=medicoId)
            querysetPAR = Capitulo.objects.aggregate(Sum('puntos'))
            if querysetPAR['puntos__sum'] is None:
                raise ResponseError('No hay capítulos', 404)
            puntosAReunir = querysetPAR['puntos__sum']
            querysetPO = RecertificacionItemDocumento.objects.filter(medico=medicoId, estatus=1).aggregate(Sum('puntosOtorgados'))
            if querysetPO['puntosOtorgados__sum'] is None:
                raise ResponseError('No hay documentos', 404)
            puntosObtenidos = querysetPO['puntosOtorgados__sum']
            porcentaje = round(puntosObtenidos * 100 / puntosAReunir, 2)
            nombreCompleto = datosMedico.nombre + ' ' + datosMedico.apPaterno + ' ' + datosMedico.apMaterno
            porcentageGeneralMedico = PorcentajeGeneralMedico(nombreCompleto, datosMedico.numRegistro, porcentaje, puntosObtenidos, puntosAReunir)
            serializer = PorcentajeGeneralMedicoSerializer(porcentageGeneralMedico)
            return Response(serializer.data)
        except Medico.DoesNotExist:
            raise ResponseError('Médico no encontrado', 404)


class PuntosPorCapituloMedicoDetailView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        capituloId = kwargs['capituloId']
        try:
            queryset = Capitulo.objects.get(id=capituloId)
            puntos = queryset.puntos
            querysetPO = RecertificacionItemDocumento.objects.filter(medico=medicoId, item__subcapitulo__capitulo=capituloId, estatus=1).aggregate(Sum('puntosOtorgados'))
            if querysetPO['puntosOtorgados__sum'] is None:
                raise ResponseError('Médico no encontrado', 404)
            reunidos = querysetPO['puntosOtorgados__sum']
            isExcedido = True if reunidos > puntos else False
            faltantes = round(puntos - reunidos, 2) if not isExcedido else 0
            excedentes = abs(round(puntos - reunidos, 2)) if isExcedido else 0
            puntosPorCapituloMedico = PuntosPorCapituloMedico(queryset.titulo, queryset.descripcion, reunidos, faltantes, isExcedido, excedentes, puntos)
            serializer = PuntosPorCapituloMedicoSerializer(puntosPorCapituloMedico)
            return Response(serializer.data)
        except Capitulo.DoesNotExist:
            raise ResponseError('Capítulo no encontrado', 404)


class DetallesCapituloDetailView(RetrieveAPIView):
    queryset = Capitulo.objects.filter()
    serializer_class = DetallesCapituloSerializer


class ItemDocumentosListView(ListAPIView):
    serializer_class = ItemDocumentosSerializer

    def get_queryset(self):
        itemId = self.kwargs['itemId']
        queryset = RecertificacionItemDocumento.objects.filter(item=itemId)
        if not queryset:
            raise ResponseError('No hay documentos', 404)
        # print(f'--->>>queryset: {queryset is None}')
        # print(f'--->>>queryset: {not queryset}')
        return queryset


class ItemDocumentosCreateView(CreateAPIView):
    serializer_class = ItemDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request.data['estatus'] = 3
        request.data['puntosOtorgados'] = 0
        request.data['observaciones'] = ''
        request.data['notasRechazo'] = ''
        request.data['razonRechazo'] = ''
        serializer = ItemDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class CertificadosMedicoListView(ListAPIView):
    serializer_class = CertificadosMedicoListSerialializer

    def get_queryset(self):
        medicoId = self.kwargs['medicoId']
        queryset = Certificado.objects.filter(medico=medicoId)
        if not queryset:
            raise ResponseError('No hay certificados', 404)
        return queryset
