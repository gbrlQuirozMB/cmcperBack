from .models import *
from .serializers import *

from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter

from api.Paginacion import Paginacion
from rest_framework.response import Response


# Create your views here.


class CertificadosFilter(FilterSet):
    nombreNS = CharFilter(field_name='medico__nombre', lookup_expr='iexact')
    apPaternoNS = CharFilter(field_name='medico__apPaterno', lookup_expr='iexact')

    class Meta:
        model = Certificado
        fields = ['nombreNS', 'apPaternoNS', 'estatus', 'id']


class CertificadosFilteredListView(ListAPIView):
    queryset = Certificado.objects.all()
    # queryset = Certificado.objects.filter(documento__isnull=False)
    # queryset = Certificado.objects.filter(documento__exact='')
    serializer_class = CertificadosFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CertificadosFilter
    # filterset_fields = ['estatus']


class CertificadoSubirDocumentoUpdateView(UpdateAPIView):
    queryset = Certificado.objects.filter()
    serializer_class = CertificadoDocumentoSerializer
    http_method_names = ['put']
