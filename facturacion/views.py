from django.shortcuts import render
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import status, permissions
from .serializers import *
from instituciones.models import *

class ConceptoPagoListView(ListAPIView):
    queryset = ConceptoPago.objects.all()
    serializer_class = ConceptoPagoSerializer

class MonedaListView(ListAPIView):
    queryset = Moneda.objects.all()
    serializer_class = MonedaSerializer

class FormaPagoListView(ListAPIView):
    queryset = FormaPago.objects.all()
    serializer_class = FormaPagoSerializer

class UsoCFDIListView(ListAPIView):
    queryset = UsoCFDI.objects.all()
    serializer_class = UsoCFDISerializer

class AvalListView(ListAPIView):#Aval se refiere al modelo de Institucion
    queryset = Institucion.objects.all()
    serializer_class = AvalSerializer