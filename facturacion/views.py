from django.http.response import HttpResponse
from django.shortcuts import render
import rest_framework
import logging
import json
from rest_framework import exceptions
from rest_framework.views import APIView
from api.exceptions import *
from rest_framework.generics import CreateAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import CharFilter, NumberFilter, DateFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, permissions
from .serializers import *
from instituciones.models import *
from django.db.models import Value
from django.db.models.functions import Concat
import os
import base64
import ssl
from django.conf import settings
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from xml.dom import minidom
from django.core.files.base import ContentFile
from suds.client import Client
from suds.plugin import MessagePlugin
from rest_framework.response import Response
from django.core import serializers

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


class AvalFilter(FilterSet):  # Aval se refiere al modelo de Institucion
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
    nombreCompletoNS = CharFilter(method='nombreCompletoFilter')
    rfcNS = CharFilter(field_name='rfcFacturacion', lookup_expr='icontains')
    noCertificadoNS = NumberFilter(field_name='numRegistro', lookup_expr='icontains')
    isCertificadoNS = CharFilter(field_name='isCertificado')

    class Meta:
        model = Medico
        fields = ['nombreCompletoNS', 'rfcNS', 'noCertificadoNS', 'isCertificadoNS']

    def nombreCompletoFilter(self, queryset, name, value):
        queryset = Medico.objects.annotate(completo=Concat('nombre', Value(' '), 'apPaterno', Value(' '), 'apMaterno'))
        return queryset.filter(completo__icontains=value)


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
        serializer = FacturaSerializer(data=request.data)
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
                    factura=factura,
                    conceptoPago=ConceptoPago.objects.get(id=conceptoPago['idConceptoPago']),
                    cantidad=conceptoPago['cantidad']
                )
                conceptosPago.append({
                    'concepto': conceptoPagoObject,
                    'total': int(conceptoPagoObject.conceptoPago.precio) * int(conceptoPagoObject.cantidad)
                })
            datos['conceptosPago'] = conceptosPago
            crearPDF(factura, datos)
            crearXML(factura)
            enviarCorreo(factura)
            return Response(serializers.serialize('json', [factura]), status=status.HTTP_201_CREATED)
            # return self.create(request, *args, **kwargs)

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
    pisa.CreatePDF(html.encode('utf-8'), dest=pdf, encoding='utf-8')
    factura.pdf = rutaPDF
    factura.save()


def crearXML(factura):
    if factura.xmlTimbrado:
        ruta = os.path.join(settings.MEDIA_ROOT, str(factura.xmlTimbrado))
        os.remove(ruta)
        factura.xmlTimbrado = None
    factura.save()
    # CREA XML
    root = minidom.Document()
    # COMPROBANTE
    comprobante = root.createElement('cfdi:Comprobante')
    comprobante.setAttribute('xmlns:cfdi', 'http://www.sat.gob.mx/cfd/3')
    comprobante.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    comprobante.setAttribute('xsi:schemaLocation', 'http://www.sat.gob.mx/cfd/3 http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd')
    comprobante.setAttribute('Version', '3.3')
    comprobante.setAttribute('Folio', str(factura.folio))
    comprobante.setAttribute('Fecha', factura.fecha.strftime('%Y-%m-%dT%H:%M:%S'))
    comprobante.setAttribute('Moneda', str(factura.moneda.moneda))
    comprobante.setAttribute('TipoDeComprobante', 'I')
    comprobante.setAttribute('MetodoPago', 'PUE')
    comprobante.setAttribute('FormaPago', str(factura.formaPago.formaPago))
    comprobante.setAttribute('LugarExpedicion', str(factura.codigoPostal))
    comprobante.setAttribute('SubTotal', str(round(factura.subtotal, factura.moneda.decimales)))
    comprobante.setAttribute('Total', str(round(factura.total, factura.moneda.decimales)))
    root.appendChild(comprobante)
    #COMPROBANTE - EMISOR
    emisor = root.createElement('cfdi:Emisor')
    # RFC PRAR PRUEBAS
    emisor.setAttribute('Rfc', 'EKU9003173C9')
    # RFC PARA PRODUCCIÓN
    #emisor.setAttribute('Rfc', 'CMC9107125P1')
    emisor.setAttribute('Nombre', 'CMCPER')
    emisor.setAttribute('RegimenFiscal', '603')  # PERSONAS MORALES CON FINES NO LUCRATIVOS
    comprobante.appendChild(emisor)
    #COMPROBANTE - RECEPTOR
    receptor = root.createElement('cfdi:Receptor')
    receptor.setAttribute('Rfc', str(factura.rfc))
    receptor.setAttribute('Nombre', str(factura.razonSocial))
    receptor.setAttribute('UsoCFDI', str(factura.usoCFDI.usoCFDI))
    comprobante.appendChild(receptor)
    conceptosFactura = ConceptoFactura.objects.filter(factura=factura)
    if conceptosFactura.count() > 0:
        #COMPROBANTE - CONCEPTOS
        conceptos = root.createElement('cfdi:Conceptos')
        #COMPROBANTE - CONCEPTOS - CONCEPTO
        for conceptoFactura in conceptosFactura:
            concepto = root.createElement('cfdi:Concepto')
            concepto.setAttribute('Cantidad', str(conceptoFactura.cantidad))
            concepto.setAttribute('ClaveProdServ', str(conceptoFactura.conceptoPago.claveSAT))
            concepto.setAttribute('ClaveUnidad', str(conceptoFactura.conceptoPago.unidadMedida.unidadMedida))
            concepto.setAttribute('Descripcion', str(conceptoFactura.conceptoPago.conceptoPago))
            concepto.setAttribute('Importe', str(round(int(conceptoFactura.conceptoPago.precio) * int(conceptoFactura.cantidad), factura.moneda.decimales)))
            concepto.setAttribute('ValorUnitario', str(conceptoFactura.conceptoPago.precio))
            if factura.iva is not None:
                #COMPROBANTE - CONCEPTOS - CONCEPTO - IMPUESTOS
                totalTraslados = 0
                impuestos = root.createElement('cfdi:Impuestos')
                #COMPROBANTE - CONCEPTOS - CONCEPTO - IMPUESTOS - TRASLADOS
                traslados = root.createElement('cfdi:Traslados')
                #COMPROBANTE - CONCEPTOS - CONCEPTO - IMPUESTOS - TRASLADOS - TRASLADO
                traslado = root.createElement('cfdi:Traslado')
                traslado.setAttribute('Base', str(round(int(conceptoFactura.conceptoPago.precio) * int(conceptoFactura.cantidad), factura.moneda.decimales)))
                traslado.setAttribute('Importe', '16.00')
                traslado.setAttribute('Impuesto', '002')
                traslado.setAttribute('TasaOCuota', '0.160000')
                traslado.setAttribute('TipoFactor', 'Tasa')
                traslados.appendChild(traslado)
                impuestos.appendChild(traslados)
                concepto.appendChild(impuestos)
            conceptos.appendChild(concepto)
        comprobante.appendChild(conceptos)
        if factura.iva is not None:
            #COMPROBANTE - IMPUESTOS
            impuestos = root.createElement('cfdi:Impuestos')
            impuestos.setAttribute('TotalImpuestosTrasladados', str(round(factura.iva, factura.moneda.decimales)))
            #COMPROBANTE - IMPUESTOS - TRASLADOS
            traslados = root.createElement('cfdi:Traslados')
            #COMPROBANTE - IMPUESTOS - TRASLADOS - TRASLADO
            traslado = root.createElement('cfdi:Traslado')
            traslado.setAttribute('Importe', str(round(factura.iva, factura.moneda.decimales)))
            traslado.setAttribute('Impuesto', '002')
            traslado.setAttribute('TasaOCuota', '0.160000')
            traslado.setAttribute('TipoFactor', 'Tasa')
            traslados.appendChild(traslado)
            impuestos.appendChild(traslados)
            comprobante.appendChild(impuestos)
    facturar(factura, root)


def facturar(factura, root):
    # DATOS PARA PRUEBAS
    url = "https://demo-facturacion.finkok.com/servicios/soap/stamp.wsdl"
    usuario = 'clientedeprueba'
    contrasena = '20cf7fc55fd9e99021840be6dac7ffdb48e96ef67d83d357de4b0a9e2fa7'
    # DATOS PARA PRODUCCIÓN
    """ url = "https://facturacion.finkok.com/servicios/soap/stamp.wsdl"
    usuario = ''
    contrasena = '' """
    # COMIENZA A FACTURAR
    xmlstr = root.toxml(encoding="utf-8")
    encodedBytes = base64.b64encode(xmlstr)
    encodedStr = str(encodedBytes, "utf-8")
    context = ssl._create_unverified_context()
    ssl._create_default_https_context = ssl._create_unverified_context
    client = Client(url, cache=None)
    xmlSAT = None
    contenido = client.service.sign_stamp(encodedStr, usuario, contrasena)
    # OBTIENE XMLSAT
    xmlSAT = contenido.xml
    if xmlSAT is not None:
        # OBTIENE DATOS DE XMLSAT
        xmlParsed = minidom.parseString(str(xmlSAT))
        comprobante = xmlParsed.getElementsByTagName('cfdi:Comprobante')[0]
        complemento = comprobante.getElementsByTagName('cfdi:Complemento')[0]
        timbre = complemento.getElementsByTagName('tfd:TimbreFiscalDigital')[0]
        uuid = timbre.getAttribute("UUID")
        selloSAT = timbre.getAttribute("SelloSAT")
        numeroCertificado = comprobante.getAttribute("NoCertificado")
        fechaTimbrado = timbre.getAttribute("FechaTimbrado")
        fechaTimbradoStr = datetime.strptime(fechaTimbrado, '%Y-%m-%dT%H:%M:%S')
        # GUARDA DATOS DE XMLSAT EN FACTURA
        factura.uuid = uuid
        factura.numeroCertificado = numeroCertificado
        factura.selloSAT = selloSAT
        factura.fechaTimbrado = fechaTimbrado
        factura.xmlTimbrado.save(factura.folio + ".xml", ContentFile(str(xmlSAT)))
        factura.save()


def enviarCorreo(factura):
    email = ''
    if factura.institucion:
        email = factura.institucion.email
    else:
        email = factura.medico.email
    html_content = render_to_string('email.html', {'nombre': factura.razonSocial, 'hoy': datetime.now().year})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives('CMCPER', text_content, 'admin@cmcper.com.mx', [email])
    email.attach_alternative(html_content, 'text/html')
    email.attach(str(factura.folio) + '.pdf', open(factura.pdf, 'rb').read(), 'application/pdf')
    if factura.xmlTimbrado:
        email.attach(str(factura.folio) + '.xml', open(factura.xmlTimbrado, 'rb').read(), 'application/xml')
    email.send()


class MyPlugin(MessagePlugin):
    def __init__(self):
        self.lastSentStr = None
        self.lastReceivedStr = None

    def sending(self, context):
        self.lastSentStr = str(context.envelope)

    def received(self, context):
        self.lastReceivedStr = str(context.reply)


def cancelarFactura(factura):
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.DEBUG)
    logging.getLogger('suds.transport').setLevel(logging.DEBUG)
    logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
    logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)
    # DATOS PARA PRUEBAS
    url = "https://demo-facturacion.finkok.com/servicios/soap/cancel.wsdl"
    usuario = 'clientedeprueba'
    contrasena = '20cf7fc55fd9e99021840be6dac7ffdb48e96ef67d83d357de4b0a9e2fa7'
    certificado = '30001000000400002434'
    emisor = 'EKU9003173C9'
    # DATOS PARA PRODUCCIÓN
    """ url = "https://facturacion.finkok.com/servicios/soap/cancel.wsdl"
        usuario = ''
        contrasena = ''
        certificado = ''
        emisor = 'CMC9107125P1' """
    facturas = [factura.uuid]
    context = ssl._create_unverified_context()
    ssl._create_default_https_context = ssl._create_unverified_context
    plugin = MyPlugin()
    client = Client(url, cache=None, plugins=[plugin])
    listaFacturas = client.factory.create("UUIDS")
    listaFacturas.uuids = {"string": facturas}
    result = client.service.sign_cancel(listaFacturas, usuario, contrasena, emisor, certificado)
    try:
        xml = plugin.lastReceivedStr[2: len(plugin.lastReceivedStr) - 1]
        factura.xmlCancelado.save(factura.folio + ".xml", ContentFile(str(xml)))
        return True
    except:
        return False


class FacturaFilter(FilterSet):
    rfcNS = CharFilter(field_name='rfc', lookup_expr='icontains')
    fechaInicioNS = DateFilter(field_name='fecha', lookup_expr="gte")
    fechaFinNS = DateFilter(field_name='fecha', lookup_expr="lte")
    concepto = CharFilter(field_name='facturaCF__conceptoPago')

    class Meta:
        model = Factura
        fields = ['rfcNS', 'fechaInicioNS', 'fechaInicioNS', 'tipo', 'concepto', 'isCancelada', 'formaPago', 'metodoPago']


class FacturaPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20


class FacturaFilteredListView(ListAPIView):
    queryset = Factura.objects.all()
    serializer_class = FacturaFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FacturaFilter
    pagination_class = FacturaPagination


class FacturaCancelarView(APIView):
    def post(self, request):
        factura = Factura.objects.get(id=request.data['id'])
        if cancelarFactura(factura):
            Factura.objects.filter(id=request.data['id']).update(isCancelada=True)
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_417_EXPECTATION_FAILED)


class MetodoPagoListView(ListAPIView):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoListSerializer
