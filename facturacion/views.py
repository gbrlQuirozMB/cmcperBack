from django.shortcuts import render
import rest_framework
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import CharFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, permissions
from .serializers import *
from instituciones.models import *

class ConceptoPagoListView(ListAPIView):
    queryset = ConceptoPago.objects.all()
    serializer_class = ConceptoPagoListSerializer

class MonedaListView(ListAPIView):
    queryset = Moneda.objects.all()
    serializer_class = MonedaListSerializer

class FormaPagoListView(ListAPIView):
    queryset = FormaPago.objects.all()
    serializer_class = FormaPagoListSerializer

class UsoCFDIListView(ListAPIView):
    queryset = UsoCFDI.objects.all()
    serializer_class = UsoCFDIListSerializer

class AvalFilter(FilterSet):#Aval se refiere al modelo de Institucion
    nombreInstitucionNS = CharFilter(field_name='nombreInstitucion', lookup_expr='icontains')
    class Meta:
        model = Institucion
        fields = ['nombreInstitucionNS']

class AvalPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20

class AvalFilteredListView(ListAPIView):
    queryset = Institucion.objects.all()
    serializer_class = AvalFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AvalFilter
    pagination_class = AvalPagination

class MedicoFilter(FilterSet):
    nombreNS = CharFilter(field_name='nombre', lookup_expr='icontains')
    apPaternoNS = CharFilter(field_name='apPaterno', lookup_expr='icontains')
    apMaternoNS = CharFilter(field_name='apMaterno', lookup_expr='icontains')
    rfcNS = CharFilter(field_name='rfc', lookup_expr='icontains')
    isCertificadoNS = CharFilter(field_name='isCertificado')
    class Meta:
        model = Medico
        fields = ['nombreNS', 'apPaternoNS', 'apMaternoNS', 'rfcNS', 'isCertificadoNS']

class MedicoPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20

class MedicoFilteredListView(ListAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedicoFilter
    pagination_class = MedicoPagination