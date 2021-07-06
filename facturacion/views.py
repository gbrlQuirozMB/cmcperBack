from django.shortcuts import render
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import status, permissions
from .serializers import *

class ConceptoPagoListView(ListAPIView):
    queryset = ConceptoPago.objects.all()
    serializer_class = ConceptoPagoSerializer