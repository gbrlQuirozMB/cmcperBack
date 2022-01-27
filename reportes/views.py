from rest_framework.pagination import PageNumberPagination
import urllib3
from rest_framework.views import APIView

from api.exceptions import *
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

from rest_framework.response import Response
import logging
log = logging.getLogger('django')


# Create your views here.


class ReportesPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20


class MedResidenteFilter(FilterSet):
    nombreCompletoNS = CharFilter(method='nombreCompletoFilter')
    hospitalResiNS = CharFilter(field_name='hospitalResi', lookup_expr='icontains')
    estadoNS = CharFilter(field_name='estado', lookup_expr='icontains')
    anioInscr = CharFilter(field_name='creado_en', lookup_expr='icontains')
    sede = CharFilter(field_name='medicoE__catSedes')
    convocatoria = CharFilter(field_name='medicoE__convocatoria')
    ciudadNS = CharFilter(field_name='ciudad', lookup_expr='icontains')

    class Meta:
        model = Medico
        fields = ['nombreCompletoNS', 'hospitalResiNS', 'estadoNS', 'sexo', 'anioInscr', 'isCertificado', 'sede', 'convocatoria',
                  'ciudadNS', 'estudioExtranjero', 'isExtranjero']

    def nombreCompletoFilter(self, queryset, name, value):
        queryset = Medico.objects.annotate(completo=Concat('nombre', Value(' '), 'apPaterno', Value(' '), 'apMaterno'))
        return queryset.filter(completo__icontains=value)


class MedResidenteFilteredListView(ListAPIView):
    queryset = Medico.objects.filter(isCertificado=False)
    serializer_class = MedResidenteListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedResidenteFilter
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = ReportesPagination

    # def get_queryset(self):
    #     queryset = Medico.objects.filter(isCertificado=False)
    #     return queryset


class MedResidenteDetailView(RetrieveAPIView):
    queryset = Medico.objects.filter(isCertificado=False)
    serializer_class = MedResidenteSerializer
    permission_classes = (permissions.IsAdminUser,)


# para un solo medico en una sola convocatoria
class MedResidenteExtrasDetailView(RetrieveAPIView):
    queryset = ConvocatoriaEnrolado.objects.filter()
    serializer_class = MedResidenteExtrasDetailSerializer
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
    # isConsejero = CharFilter(field_name='isConsejero')
    # isProfesor = CharFilter(field_name='isProfesor')

    class Meta:
        model = Medico
        fields = ['nombreCompletoNS', 'telCelularNS', 'emailNS', 'numRegistro', 'hospitalResiNS', 'estadoNS', 'sexo', 'anioCertificacion', 'estatus', 'isConsejero', 'isProfesor', 'isCertificado']

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
    pagination_class = ReportesPagination


class MedCertificadoDetailView(RetrieveAPIView):
    queryset = Medico.objects.filter(isCertificado=True)
    serializer_class = MedCertificadoSerializer
    permission_classes = (permissions.IsAdminUser,)


class MedCertificadoFechasDetailView(RetrieveAPIView):
    serializer_class = MedCertificadoFechasSerializer

    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        try:
            queryset = Certificado.objects.filter(medico=medicoId)[0]
            serializer = MedCertificadoFechasSerializer(queryset)
        except:
            raise ResponseError('No hay certificado para el ID de Medico dado', 404)

        return Response(serializer.data)


# class PruebasPdfDetailView(APIView):
#     permission_classes = (permissions.AllowAny,)

#     def get(self, request, *args, **kwargs):
#         medicoId = kwargs['medicoId']
#         http = urllib3.PoolManager()
#         url = f'http://127.0.0.1:8080/reportes/medico/{medicoId}/'
#         print(f'--->>>url: {url}')
#         r = http.request('GET', url)
#         return Response(r.data)


class MedResidenteDocumentosFilter(FilterSet):
    class Meta:
        model = ConvocatoriaEnrolado
        fields = ['convocatoria']


class MedResidenteDocumentosFilteredListView(ListAPIView):
    queryset = ConvocatoriaEnrolado.objects.all()
    serializer_class = MedResidenteDocumentosFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedResidenteDocumentosFilter


class DirectorioFilter(FilterSet):
    class Meta:
        model = Medico
        fields = ['isCertificado']


class DirectorioFilteredListView(ListAPIView):
    queryset = Medico.objects.all()
    serializer_class = DirectorioListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DirectorioFilter
    pagination_class = ReportesPagination
    permission_classes = (permissions.AllowAny,)
    
    