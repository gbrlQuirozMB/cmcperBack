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
        try:
            queryset = Certificado.objects.filter(medico=medicoId)[0]
            serializer = CertificadoDatosSerializer(queryset)
        except:
            raise ResponseError('No hay certificado para el ID de Medico dado', 404)

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
    queryset = Capitulo.objects.all().order_by('id')
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


def getQuerysetItemDocumentosFiltered(estatus, nombre, apPaterno):
    # queryset = RecertificacionItemDocumento.objects.filter(estatus=estatus, medico__nombre__iexact=nombre, medico__apPaterno__iexact=apPaterno)
    if nombre == 'all' and apPaterno == 'all' and estatus == '0':
        queryset = RecertificacionItemDocumento.objects.filter()
        return queryset

    if nombre == 'all' and apPaterno == 'all' and estatus != '0':
        queryset = RecertificacionItemDocumento.objects.filter(estatus=estatus)
        return queryset

    if nombre == 'all' and apPaterno != 'all' and estatus == '0':
        queryset = RecertificacionItemDocumento.objects.filter(medico__apPaterno__iexact=apPaterno)
        return queryset

    if nombre == 'all' and apPaterno != 'all' and estatus != '0':
        queryset = RecertificacionItemDocumento.objects.filter(medico__apPaterno__iexact=apPaterno, estatus=estatus)
        return queryset

    if nombre != 'all' and apPaterno == 'all' and estatus == '0':
        queryset = RecertificacionItemDocumento.objects.filter(medico__nombre__iexact=nombre)
        return queryset

    if nombre != 'all' and apPaterno == 'all' and estatus != '0':
        queryset = RecertificacionItemDocumento.objects.filter(medico__nombre__iexact=nombre, estatus=estatus)
        return queryset

    if nombre != 'all' and apPaterno != 'all' and estatus == '0':
        queryset = RecertificacionItemDocumento.objects.filter(medico__nombre__iexact=nombre, medico__apPaterno__iexact=apPaterno)
        return queryset

    if nombre != 'all' and apPaterno != 'all' and estatus != '0':
        queryset = RecertificacionItemDocumento.objects.filter(medico__nombre__iexact=nombre, medico__apPaterno__iexact=apPaterno, estatus=estatus)
        return queryset


class ItemDocumentosFilteredListView(ListAPIView):
    serializer_class = ItemDocumentoFilteredSerializer

    def get_queryset(self):
        estatus = self.kwargs['estatus']
        nombre = self.kwargs['nombre']
        apPaterno = self.kwargs['apPaterno']
        log.info(f'se busca por:  estatus: {estatus} - nombre: {nombre} - apPaterno: {apPaterno}')

        return getQuerysetItemDocumentosFiltered(estatus, nombre, apPaterno)


class ItemDocumentosDetailView(RetrieveAPIView):
    queryset = RecertificacionItemDocumento.objects.filter()
    serializer_class = ItemDocumentoDetailSerializer


class ItemDocumentosAceptar(UpdateAPIView):
    queryset = RecertificacionItemDocumento.objects.filter()
    serializer_class = ItemDocumentoAceptarRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        request.data['estatus'] = 1
        request.data['notasRechazo'] = ''
        request.data['razonRechazo'] = ''

        return self.update(request, *args, **kwargs)


class ItemDocumentosRechazar(UpdateAPIView):
    queryset = RecertificacionItemDocumento.objects.filter()
    serializer_class = ItemDocumentoAceptarRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        request.data['estatus'] = 2
        request.data['puntosOtorgados'] = 0

        return self.update(request, *args, **kwargs)


class ItemDocumentosReasignar(UpdateAPIView):
    queryset = RecertificacionItemDocumento.objects.filter()
    serializer_class = ItemDocumentoReasignarSerializer
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        request.data['estatus'] = 1
        request.data['notasRechazo'] = ''
        request.data['razonRechazo'] = ''

        return self.update(request, *args, **kwargs)


class CapituloListView(ListAPIView):
    queryset = Capitulo.objects.all()
    serializer_class = CapituloListSerializer


class SubcapituloListView(ListAPIView):
    serializer_class = SubcapituloListSerializer

    def get_queryset(self):
        capituloId = self.kwargs['capituloId']
        queryset = Subcapitulo.objects.filter(capitulo=capituloId)
        if not queryset:
            raise ResponseError('No existen subcapitulos con el capituloId proporcionado', 404)
        return queryset


class ItemListView(ListAPIView):
    serializer_class = ItemListSerializer

    def get_queryset(self):
        subcapituloId = self.kwargs['subcapituloId']
        queryset = Item.objects.filter(subcapitulo=subcapituloId)
        if not queryset:
            raise ResponseError('No existen items con el subcapituloId proporcionado', 404)
        return queryset
