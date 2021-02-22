import re
from rest_framework import response, status
from rest_framework.views import APIView
from .serializers import *
from preregistro.models import Medico
from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from api.logger import log
from api.exceptions import *
from rest_framework import permissions
import json
from datetime import date

# Create your views here.


class EsExtranjeroUpdateView(UpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = EsExtranjeroSerializer

    def put(self, request, *args, **kwargs):
        # para poder modificar el dato que llega
        request.data._mutable = True
        request.data['isExtranjero'] = True
        request.data._mutable = False

        return self.update(request, *args, **kwargs)


class EstudioExtranjeroUpdateView(UpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = EstudioExtranjeroSerializer

    def put(self, request, *args, **kwargs):
        # para poder modificar el dato que llega
        request.data._mutable = True
        request.data['estudioExtranjero'] = True
        request.data._mutable = False

        return self.update(request, *args, **kwargs)


class ConvocatoriaCreateView(CreateAPIView):
    serializer_class = ConvocatoriaSerializer

    def post(self, request, *args, **kwargs):
        serializer = ConvocatoriaSerializer(data=request.data)
        campoSedes = request.data.get('sedes')
        if campoSedes is None:
            log.info(f'campos incorrectos: sedes')
            raise CamposIncorrectos({"sedes": ["Este campo es requerido"]})
        campoTiposExamen = request.data.get('tiposExamen')
        if campoTiposExamen is None:
            log.info(f'campos incorrectos: tiposExamen')
            raise CamposIncorrectos({"tiposExamen": ["Este campo es requerido"]})
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class ConvocatoriaListView(ListAPIView):
    queryset = Convocatoria.objects.filter(fechaTermino__gte=date.today())
    serializer_class = ConvocatoriaListSerializer


class ConvocatoriaDetailView(RetrieveAPIView):
    queryset = Convocatoria.objects.filter()
    serializer_class = ConvocatoriaGetDetailSerializer


class ConvocatoriaArchivoUpdateView(UpdateAPIView):
    queryset = Convocatoria.objects.filter()
    serializer_class = ConvocatoriaArchivoSerializer


class ConvocatoriaBannerUpdateView(UpdateAPIView):
    queryset = Convocatoria.objects.filter()
    serializer_class = ConvocatoriaBannerSerializer


class ConvocatoriaUpdateView(UpdateAPIView):
    queryset = Convocatoria.objects.filter()
    serializer_class = ConvocatoriaSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ConvocatoriaDeleteView(DestroyAPIView):
    queryset = Convocatoria.objects.filter()


class ConvocatoriaEnroladoCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoSerializer

    def post(self, request, *args, **kwargs):
        request.data['isPagado'] = False
        request.data['comentario'] = ''
        request.data['isAceptado'] = False
        serializer = ConvocatoriaEnroladoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


def inicializaData(request):
    request.data['isValidado'] = False
    request.data['engargoladoOk'] = False
    request.data['notasValidado'] = ''
    request.data['notasEngargolado'] = ''
    request.data['rechazoValidado'] = ''
    request.data['rechazoEngargolado'] = ''
    return request


class DocumentoRevalidacionCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 1
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCurpCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 2
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoActaNacimientoCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 3
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCartaSolicitudCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 4
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoConstanciaPosgradoCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 5
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCedulaEspecialidadCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 6
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoTituloLicenciaturaCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 7
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCedulaProfesionalCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 8
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoConstanciaCirugiaCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 9
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCartaProfesorCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 10
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentosMedicoListView(ListAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoListSerializer

    def get_queryset(self):
        medicoId = self.kwargs['medicoId']
        queryset = ConvocatoriaEnroladoDocumento.objects.filter(medico=medicoId)
        return queryset


class ConvocatoriaDocumentoUpdateView(UpdateAPIView):
    queryset = ConvocatoriaEnroladoDocumento.objects.filter()
    serializer_class = ConvocatoriaDocumentoSerializer
