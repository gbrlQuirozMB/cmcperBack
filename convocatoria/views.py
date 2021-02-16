from rest_framework import response, status
from rest_framework.views import APIView
from .serializers import *
from preregistro.models import Medico
from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from api.logger import log
from api.exceptions import *
from rest_framework import permissions
import json
from datetime import date



# import json
# from rest_framework.parsers import BaseParser, DataAndFiles
# from django.conf import settings
# from django.http.multipartparser import MultiPartParser as DjangoMultiPartParser, MultiPartParserError
# # from django.utils import six
# from rest_framework.exceptions import ParseError


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
            raise CamposIncorrectos({"sedes": ["Este campo es requerido"]})
        campoTipoExamenes = request.data.get('tipoExamenes')
        if campoTipoExamenes is None:
            raise CamposIncorrectos({"tipoExamenes": ["Este campo es requerido"]})
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class ConvocatoriaListView(ListAPIView):
    queryset = Convocatoria.objects.filter(fechaTermino__gte=date.today())
    serializer_class = ConvocatoriaListSerializer
    
    
class ConvocatoriaDetailView(RetrieveAPIView):
    queryset = Convocatoria.objects.filter()
    serializer_class =  ConvocatoriaGetDetailSerializer