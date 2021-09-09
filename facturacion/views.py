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
from xml.dom import minidom
from django.core.files.base import ContentFile

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
            #crearPDF(factura, datos)
            crearXML(factura)
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

def enviarCorreo(factura):
    email = ''
    if factura.institucion:
        email = factura.institucion.email
    else:
        email = factura.medico.email
    html_content = render_to_string('email.html', {'nombre' : factura.razonSocial, 'hoy' : datetime.now().year})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives('CMCPER', text_content, 'admin@cmcper.com.mx', [email])
    email.attach_alternative(html_content, 'text/html')
    email.attach(str(factura.folio) + '.pdf', open(factura.pdf, 'rb').read(), 'application/pdf')

def crearXML(factura):
    if factura.xmlTimbrado:
        ruta = os.path.join(settings.MEDIA_ROOT, str(factura.xmlTimbrado))
        os.remove(ruta)
        factura.xmlTimbrado = None
    factura.save()
    #CREA XML
    root = minidom.Document()
    #COMPROBANTE
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
    #emisor.setAttribute('Rfc', 'TTA1511107W5')
    emisor.setAttribute('Rfc', 'EKU9003173C9')
    emisor.setAttribute('Nombre', 'CMCPER')
    emisor.setAttribute('RegimenFiscal', '624')
    comprobante.appendChild(emisor)
    #COMPROBANTE - RECEPTOR
    receptor = root.createElement('cfdi:Receptor')
    receptor.setAttribute('Rfc', str(factura.rfc))
    receptor.setAttribute('Nombre', str(factura.razonSocial))
    receptor.setAttribute('UsoCFDI', str(factura.usoCFDI.usoCFDI))
    comprobante.appendChild(receptor)
    conceptosFactura = ConceptoFactura.objects.filter(factura = factura)
    if conceptosFactura.count() > 0:
        #COMPROBANTE - CONCEPTOS
        conceptos = root.createElement('cfdi:Conceptos')
        #COMPROBANTE - CONCEPTOS - CONCEPTO
        for conceptoFactura in conceptosFactura:
            concepto = root.createElement('cfdi:Concepto')
            concepto.setAttribute('ClaveProdServ', str(conceptoFactura.conceptoPago.claveSAT))
            concepto.setAttribute('Cantidad', str(conceptoFactura.cantidad))
            concepto.setAttribute('ClaveUnidad', str(conceptoFactura.conceptoPago.unidadMedida.unidadMedida))
            concepto.setAttribute('Descripcion', str(conceptoFactura.conceptoPago.conceptoPago))
            concepto.setAttribute('ValorUnitario', str(conceptoFactura.conceptoPago.precio))
            concepto.setAttribute('Importe', str(round(int(conceptoFactura.conceptoPago.precio) * int(conceptoFactura.cantidad), factura.moneda.decimales)))
            #COMPROBANTE - CONCEPTOS - CONCEPTO - IMPUESTOS
            """ impuestosConcepto = ImpuestoConcepto.objects.filter(conceptoFactura = conceptoFactura)
            if impuestosConcepto.count() > 0:
                totalTraslados = 0
                totalRetenciones = 0
                impuestos = root.createElement('cfdi:Impuestos')
                impuestosConceptoTraslado = impuestosConcepto.filter(tipoImpuesto = 1)
                if impuestosConceptoTraslado.count() > 0:
                    #COMPROBANTE - CONCEPTOS - CONCEPTO - IMPUESTOS - TRASLADOS
                    traslados = root.createElement('cfdi:Traslados')
                    for impuestoConceptoTraslado in impuestosConceptoTraslado:
                        #COMPROBANTE - CONCEPTOS - CONCEPTO - IMPUESTOS - TRASLADOS - TRASLADO
                        traslado = root.createElement('cfdi:Traslado')
                        traslado.setAttribute('Base', str(round(impuestoConceptoTraslado.base, factura.moneda.decimales)))
                        traslado.setAttribute('Impuesto', '00' + str(impuestoConceptoTraslado.impuesto))
                        if impuestoConceptoTraslado.factor == 1:
                            factor = 'Tasa'
                        if impuestoConceptoTraslado.factor == 2:
                            factor = 'Cuota'
                        if impuestoConceptoTraslado.factor == 3:
                            factor = 'Exento'
                        traslado.setAttribute('TipoFactor', factor)
                        if impuestoConceptoTraslado.factor != 3:
                            traslado.setAttribute('TasaOCuota', str(impuestoConceptoTraslado.tasa))
                            traslado.setAttribute('Importe', str(round(impuestoConceptoTraslado.importe, factura.moneda.decimales)))
                        traslados.appendChild(traslado)
                        totalTraslados = totalTraslados + impuestoConceptoTraslado.importe
                    impuestos.appendChild(traslados)
                concepto.appendChild(impuestos) """
            conceptos.appendChild(concepto)
        comprobante.appendChild(conceptos)
        """ if impuestosConcepto.count() > 0:
            #COMPROBANTE - IMPUESTOS
            impuestos = root.createElement('cfdi:Impuestos')
            if totalRetenciones > 0:
                impuestos.setAttribute('TotalImpuestosRetenidos', str(round(totalRetenciones, factura.moneda.decimales)))
            if totalTraslados > 0:
                impuestos.setAttribute('TotalImpuestosTrasladados', str(round(totalTraslados, factura.moneda.decimales)))
            if impuestosConceptoRetencion.count() > 0:
                #COMPROBANTE - IMPUESTOS - RETENCIONES
                retenciones = root.createElement('cfdi:Retenciones')
                for impuestoConceptoRetencion in impuestosConceptoRetencion:
                    #COMPROBANTE - IMPUESTOS - RETENCIONES - RETENCION
                    retencion = root.createElement('cfdi:Retencion')
                    retencion.setAttribute('Impuesto', '00' + str(impuestoConceptoRetencion.impuesto))
                    if impuestoConceptoTraslado.factor != 3:
                        retencion.setAttribute('Importe', str(round(impuestoConceptoRetencion.importe, factura.moneda.decimales)))
                    retenciones.appendChild(retencion)
                impuestos.appendChild(retenciones)
            if impuestosConceptoTraslado.count() > 0:
                #COMPROBANTE - IMPUESTOS - TRASLADOS
                traslados = root.createElement('cfdi:Traslados')
                for impuestoConceptoTraslado in impuestosConceptoTraslado:
                    #COMPROBANTE - IMPUESTOS - TRASLADOS - TRASLADO
                    traslado = root.createElement('cfdi:Traslado')
                    traslado.setAttribute('Impuesto', '00' + str(impuestoConceptoTraslado.impuesto))
                    if impuestoConceptoTraslado.factor == 1:
                        factor = 'Tasa'
                    if impuestoConceptoTraslado.factor == 2:
                        factor = 'Cuota'
                    if impuestoConceptoTraslado.factor == 3:
                        factor = 'Exento'
                    traslado.setAttribute('TipoFactor', factor)
                    if impuestoConceptoTraslado.factor != 3:
                        traslado.setAttribute('TasaOCuota', str(impuestoConceptoTraslado.tasa))
                        traslado.setAttribute('Importe', str(round(impuestoConceptoTraslado.importe, factura.moneda.decimales)))
                    traslados.appendChild(traslado)
                impuestos.appendChild(traslados)
            comprobante.appendChild(impuestos) """
    #GUARDA XML
    xml = root.toprettyxml(encoding = "utf-8")
    factura.xmlTimbrado.save(factura.folio + ".xml", ContentFile(xml))