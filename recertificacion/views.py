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
class CertificadoDatosDetailView(RetrieveAPIView):
    serializer_class = CertificadoDatosSerializer
    lookup_field = 'medico'
    lookup_url_kwarg = 'medicoId'

    def get_queryset(self):
        queryset = Certificado.objects.filter(isVencido=False)
        return queryset


class AvanceMedicoCapituloDetailView(RetrieveAPIView):
    # serializer_class = AvanceMedicoCapituloSerializer

    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        capituloId = kwargs['capituloId']
        try:
            datosCapitulo = Capitulo.objects.get(id=capituloId)
            queryset = RecertificacionItemDocumento.objects.filter(medico=medicoId, item__subcapitulo__capitulo=1, estatus=1).aggregate(Sum('puntosOtorgados'))
            if queryset['puntosOtorgados__sum'] is None:
                respuesta = {"detail": "Médico no encontrado"}
                return Response(respuesta, status=status.HTTP_404_NOT_FOUND)
            puntosOtorgados = queryset['puntosOtorgados__sum']
            avance = round(puntosOtorgados * 100 / datosCapitulo.puntos,2)
            avanceMedicoCapitulo = AvanceMedicoCapitulo(datosCapitulo.descripcion, datosCapitulo.puntos, puntosOtorgados, avance)
            serializer = AvanceMedicoCapituloSerializer(avanceMedicoCapitulo)    
            # return Response(JSONRenderer().render(serializer.data))
            return Response(serializer.data)    
        except Capitulo.DoesNotExist:
            respuesta = {"detail": "Capítulo no encontrado"}
            return Response(respuesta, status=status.HTTP_404_NOT_FOUND)
        
        
        
