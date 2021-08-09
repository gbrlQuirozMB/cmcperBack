from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter

from .serializers import *

from preregistro.models import Medico

from django.db.models import Q


# Create your views here.


class MedResidenteFilter(FilterSet):
    telConsultorioNS = CharFilter(field_name='telConsultorio', lookup_expr='icontains')
    telParticularNS = CharFilter(field_name='telParticular', lookup_expr='icontains')
    telJefEnseNS = CharFilter(field_name='telJefEnse', lookup_expr='icontains')
    emailNS = CharFilter(field_name='email', lookup_expr='icontains')
    # nombreCompletoNS = CharFilter(method='nombreCompletoFilter')

    class Meta:
        model = Medico
        # fields = ['telConsultorioNS', 'telParticularNS', 'telJefEnseNS', 'emailNS', 'sexo', 'nombreCompletoNS']
        fields = ['telConsultorioNS', 'telParticularNS', 'telJefEnseNS', 'emailNS', 'sexo', 'nombre', 'apPaterno', 'apMaterno']

    # def nombreCompletoFilter(self, queryset, name, value):
    #     # print(f'--->>>value: {value}')
    #     # return Medico.objects.filter(Q(nombre__icontains=value) | Q(apPaterno__icontains=value) | Q(apMaterno__icontains=value)) #uso de OR
    #     valSeparados = value.split(',')
    #     return Medico.objects.filter(nombre__icontains=valSeparados[0], apPaterno__icontains=valSeparados[1], apMaterno__icontains=valSeparados[2])


class MedResidenteFilteredListView(ListAPIView):
    queryset = Medico.objects.filter(isCertificado=False)
    serializer_class = MedResidenteListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedResidenteFilter


class MedResidenteDetailView(RetrieveAPIView):
    queryset = Medico.objects.filter(isCertificado=False)
    serializer_class = MedResidenteSerializer
