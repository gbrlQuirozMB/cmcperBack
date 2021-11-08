from .models import *
from .serializers import *

from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter

from api.Paginacion import Paginacion
from rest_framework.response import Response
from certificados.models import Certificado


class MedicosListView(ListAPIView):
    queryset = Certificado.objects.filter(isConacem=False)
    serializer_class = MedicosListSerializer
