from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, NumberFilter
from rest_framework import permissions

from .serializers import *

from preregistro.models import Medico
from convocatoria.models import *

from django.db.models import Q, Value
from django.db.models.functions import Concat

from datetime import date


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
    permission_classes = (permissions.IsAdminUser,)


class MedResidenteDetailView(RetrieveAPIView):
    queryset = Medico.objects.filter(isCertificado=False)
    serializer_class = MedResidenteSerializer
    permission_classes = (permissions.IsAdminUser,)


# para un solo medico en una sola convocatoria
class MedResidenteExtrasDetailView(RetrieveAPIView):
    queryset = ConvocatoriaEnrolado.objects.filter()
    serializer_class = MedResidenteExtrasDetailView
    lookup_field = 'medico'
    lookup_url_kwarg = 'medicoId'
    permission_classes = (permissions.IsAdminUser,)


# # desconozco si puedan existir varios registros de un medico en la convocatoria
# class MedResidenteExtrasDetailView(ListAPIView):
#     serializer_class = MedResidenteExtrasDetailView
#     permission_classes = (permissions.IsAdminUser,)


#     def get_queryset(self):
#         medicoId = self.kwargs['medicoId']
#         queryset = ConvocatoriaEnrolado.objects.filter(medico=medicoId).order_by('-id')[:1]

#         return queryset


class MedCertificadoFilter(FilterSet):
    nombreCompletoNS = CharFilter(method='nombreCompletoFilter')
    telCelularNS = CharFilter(field_name='telCelular', lookup_expr='icontains')
    emailNS = CharFilter(field_name='email', lookup_expr='icontains')
    numRegistro = NumberFilter(field_name='numRegistro', lookup_expr='icontains')
    hospitalResiNS = CharFilter(field_name='hospitalResi', lookup_expr='icontains')
    estadoNS = CharFilter(field_name='estado', lookup_expr='icontains')
    anioCertificacion = NumberFilter(field_name='anioCertificacion', lookup_expr='icontains')
    # estatusNS = CharFilter(method='estatusFilter')
    estatus = CharFilter(field_name='medicoC__estatus')
    # falta: tipo (profesor/consejero) -> hay que crear los campos
    isConsejero = CharFilter(field_name='isConsejero')
    isProfesor = CharFilter(field_name='isProfesor')

    class Meta:
        model = Medico
        fields = ['nombreCompletoNS', 'telCelularNS', 'emailNS', 'numRegistro', 'hospitalResiNS', 'estadoNS', 'sexo', 'anioCertificacion', 'estatus', 'isConsejero', 'isProfesor']

    def nombreCompletoFilter(self, queryset, name, value):
        queryset = Medico.objects.annotate(completo=Concat('nombre', Value(' '), 'apPaterno', Value(' '), 'apMaterno'))
        return queryset.filter(completo__icontains=value)

    # def estatusFilter(self, queryset, name, value):
    #     itemIds = []
    #     for dato in Certificado.objects.filter(estatus=value):
    #         if dato.medico.id not in itemIds:
    #             itemIds.append(dato.medico.id)
    #     return Medico.objects.filter(pk__in=itemIds)


class MedCertificadoFilteredListView(ListAPIView):
    queryset = Medico.objects.filter(isCertificado=True)
    serializer_class = MedCertificadoListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedCertificadoFilter
    permission_classes = (permissions.IsAdminUser,)
