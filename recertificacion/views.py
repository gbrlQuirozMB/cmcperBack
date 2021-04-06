from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from preregistro.models import Medico

from api.logger import log
from api.exceptions import *

from .serializers import *


# Create your views here.
class CertificadoDatosDetailView(RetrieveAPIView):
    serializer_class = CertificadoDatosSerializer
    lookup_field = 'medico'
    lookup_url_kwarg = 'medicoId'
    
    def get_queryset(self):
        queryset = Certificado.objects.filter(isVencido=False)
        return queryset