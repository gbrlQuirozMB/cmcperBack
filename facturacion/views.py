from django.http.response import HttpResponse
from django.shortcuts import render
import rest_framework, logging, json
from api.exceptions import *
from rest_framework.generics import CreateAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import CharFilter, NumberFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, permissions
from .serializers import *
from instituciones.models import *
from django.db.models import Value
from django.db.models.functions import Concat

log = logging.getLogger('django')

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
    nombreInstitucionNS = CharFilter(field_name = 'nombreInstitucion', lookup_expr = 'icontains')
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
    nombreCompletoNS = CharFilter(method = 'nombreCompletoFilter')
    rfcNS = CharFilter(field_name = 'rfcFacturacion', lookup_expr = 'icontains')
    noCertificadoNS = NumberFilter(field_name='numRegistro', lookup_expr = 'icontains')
    isCertificadoNS = CharFilter(field_name = 'isCertificado')
    class Meta:
        model = Medico
        fields = ['nombreCompletoNS', 'rfcNS', 'noCertificadoNS', 'isCertificadoNS']
    def nombreCompletoFilter(self, queryset, name, value):
        queryset = Medico.objects.annotate(completo = Concat('nombre', Value(' '), 'apPaterno', Value(' '), 'apMaterno'))
        return queryset.filter(completo__icontains = value)

class MedicoPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20

class MedicoFilteredListView(ListAPIView):
    queryset = Medico.objects.all()
    serializer_class = MedicoFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedicoFilter
    pagination_class = MedicoPagination

class IdUltimaFacturaView(ListAPIView):
    queryset = Factura.objects.all().order_by('-id')[:1]
    serializer_class = IdUltimaFacturaSerializer

class PaisListView(ListAPIView):
    queryset = Pais.objects.all()
    serializer_class = PaisListSerializer

class FacturaCreateView(CreateAPIView):
    serializer_class = FacturaSerializer
    def post(self, request, *args, **kwargs):
        print('----------------------------------------------------------------------------------------------------')
        print(request.data)
        print('----------------------------------------------------------------------------------------------------')
        print('----------------------------------------------------------------------------------------------------')
        for concepto in request.data['conceptosPago']:
            print('----------')
            print(concepto['idConceptoPago'])
            print(concepto['cantidad'])
            print('----------')
        print('----------------------------------------------------------------------------------------------------')
        serializer = FacturaSerializer(data = request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)