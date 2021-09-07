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
import os
from django.conf import settings
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from datetime import datetime

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
        serializer = FacturaSerializer(data = request.data)
        if serializer.is_valid():
            factura = serializer.save()
            if factura.institucion:
                factura.rfc = factura.institucion.rfc
                factura.razonSocial = factura.institucion.nombreInstitucion
                factura.estado = factura.institucion.estado
                factura.deleMuni = factura.institucion.deleMuni
                factura.colonia = factura.institucion.colonia
                factura.calle = factura.institucion.calle
                factura.numInterior = factura.institucion.numInterior
                factura.numExterior = factura.institucion.numExterior
                factura.codigoPostal = factura.institucion.cp
            else:
                factura.rfc = factura.medico.rfcFacturacion
                factura.razonSocial = factura.medico.razonSocial
                factura.estado = factura.medico.estadoFisc
                factura.deleMuni = factura.medico.deleMuniFisc
                factura.colonia = factura.medico.coloniaFisc
                factura.calle = factura.medico.calleFisc
                factura.numInterior = factura.medico.numInteriorFisc
                factura.numExterior = factura.medico.numExteriorFisc
                factura.codigoPostal = factura.medico.cpFisc
            factura.save()
            datos = {}
            datos['factura'] = factura
            datos['importeLetra'] = request.data['importeLetra']
            datos['agregarDireccion'] = request.data['agregarDireccion']
            datos['certificado'] = request.data['certificado']
            datos['recertificacion'] = request.data['recertificacion']
            conceptosPago = []
            for conceptoPago in request.data['conceptosPago']:
                conceptoPagoObject = ConceptoFactura.objects.create(
                    factura = factura,
                    conceptoPago = ConceptoPago.objects.get(id = conceptoPago['idConceptoPago']),
                    cantidad = conceptoPago['cantidad']
                )
                conceptosPago.append({
                    'concepto' : conceptoPagoObject,
                    'total' : int(conceptoPagoObject.conceptoPago.precio) * int(conceptoPagoObject.cantidad)
                })
            datos['conceptosPago'] = conceptosPago
            crearPDF(factura, datos)
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)

def crearPDF(factura, datos):
    try:
        os.remove(factura.pdf)
    except:
        pass
    template = get_template('pdf.html')
    html = template.render(datos)
    carpeta = 'facturasPDF/'
    try:
        os.mkdir(os.path.join(settings.MEDIA_ROOT, carpeta))
    except:
        pass
    nombreArchivo = str(factura.folio) + '.pdf'
    rutaPDF = os.path.join(settings.MEDIA_ROOT, carpeta, nombreArchivo)
    pdf = open(rutaPDF, 'wb+')
    pisa.CreatePDF(html.encode('utf-8'), dest = pdf, encoding = 'utf-8')
    factura.pdf = rutaPDF
    factura.save()
    enviarCorreo(factura, nombreArchivo)

def enviarCorreo(factura, nombreArchivo):
    email = ''
    if factura.institucion:
        email = factura.institucion.email
    else:
        email = factura.medico.email
    html_content = render_to_string('email.html', {'nombre' : factura.razonSocial, 'hoy' : datetime.now().year})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives('CMCPER', text_content, 'admin@cmcper.com.mx', [email])
    email.attach_alternative(html_content, 'text/html')
    email.attach(nombreArchivo, open(factura.pdf, 'rb').read(), 'application/pdf')