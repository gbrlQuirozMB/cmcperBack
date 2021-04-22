from django.db.models.query import EmptyQuerySet
from rest_framework import response, status, permissions
from rest_framework.views import APIView
from .serializers import *
from preregistro.models import Medico
from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView, get_object_or_404
from api.logger import log
from api.exceptions import *
import json
from datetime import date
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.response import Response

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View
import ssl

from api.Paginacion import Paginacion

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from notificaciones.models import Notificacion
from django.contrib.auth.models import User

import csv
import codecs

import locale

from recertificacion.models import Certificado

# from django_filters import rest_framework
# from django_filters import rest_framework as filters

# Create your views here.

totalDocumentosExtranjero = 10
totalDocumentosNacional = 9


class EsExtranjeroUpdateView(UpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = EsExtranjeroSerializer

    # def put(self, request, *args, **kwargs):
    #     # para poder modificar el dato que llega
    #     # request.data._mutable = True
    #     # request.data['isExtranjero'] = True
    #     # request.data._mutable = False

    #     return self.update(request, *args, **kwargs)


class EstudioExtranjeroUpdateView(UpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = EstudioExtranjeroSerializer

    # def put(self, request, *args, **kwargs):
    #     # para poder modificar el dato que llega
    #     # request.data._mutable = True
    #     # request.data['estudioExtranjero'] = True
    #     # request.data._mutable = False

    #     return self.update(request, *args, **kwargs)


class ConvocatoriaCreateView(CreateAPIView):
    serializer_class = ConvocatoriaSerializer
    # parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        serializer = ConvocatoriaSerializer(data=request.data)
        campoSedes = request.data.get('sedes')
        if campoSedes is None:
            log.info(f'campos incorrectos: sedes')
            raise CamposIncorrectos({"sedes": ["Este campo es requerido"]})
        campoTiposExamen = request.data.get('tiposExamen')
        if campoTiposExamen is None:
            log.info(f'campos incorrectos: tiposExamen')
            raise CamposIncorrectos({"tiposExamen": ["Este campo es requerido"]})
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class ConvocatoriaListView(ListAPIView):
    queryset = Convocatoria.objects.filter(fechaTermino__gte=date.today())
    serializer_class = ConvocatoriaListSerializer


class ConvocatoriaDetailView(RetrieveAPIView):
    queryset = Convocatoria.objects.filter()
    serializer_class = ConvocatoriaGetDetailSerializer


class ConvocatoriaArchivoUpdateView(UpdateAPIView):
    queryset = Convocatoria.objects.filter()
    serializer_class = ConvocatoriaArchivoSerializer


class ConvocatoriaBannerUpdateView(UpdateAPIView):
    queryset = Convocatoria.objects.filter()
    serializer_class = ConvocatoriaBannerSerializer


class ConvocatoriaUpdateView(UpdateAPIView):
    queryset = Convocatoria.objects.filter()
    serializer_class = ConvocatoriaSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ConvocatoriaDeleteView(DestroyAPIView):
    queryset = Convocatoria.objects.filter()


class ConvocatoriaEnroladoCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoSerializer

    def post(self, request, *args, **kwargs):
        medicoId = request.data['medico']
        convocatoriaId = request.data['convocatoria']
        cuenta = ConvocatoriaEnrolado.objects.filter(medico=medicoId, convocatoria=convocatoriaId).count()
        if cuenta > 0:
            log.info('Ya existe el médico enrolado a esta convocatoria')
            raise ResponseError('Ya existe el médico enrolado a esta convocatoria', 409)
        request.data['isPagado'] = False
        request.data['comentario'] = ''
        request.data['isAceptado'] = False
        serializer = ConvocatoriaEnroladoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


def inicializaData(request):
    request.data['isValidado'] = False
    request.data['engargoladoOk'] = False
    request.data['notasValidado'] = ''
    request.data['notasEngargolado'] = ''
    request.data['rechazoValidado'] = ''
    request.data['rechazoEngargolado'] = ''
    return request


def borraExistentes(request, tipoDocumento):
    medicoId = request.data['medico']
    convocatoriaId = request.data['convocatoria']
    ConvocatoriaEnroladoDocumento.objects.filter(medico=medicoId, convocatoria=convocatoriaId, catTiposDocumento=tipoDocumento).delete()


def totalDocumentosNotifica(request):
    medicoId = request.data['medico']
    convocatoriaId = request.data['convocatoria']
    estudioExtranjero = Medico.objects.filter(id=medicoId).values_list('estudioExtranjero')
    cuentaDocumentos = ConvocatoriaEnroladoDocumento.objects.filter(medico=medicoId, convocatoria=convocatoriaId).count()
    # print(f'--->>>estudioExtranjero: {estudioExtranjero[0][0]} - cuentaDocumentos: {cuentaDocumentos}')
    if estudioExtranjero[0][0] and cuentaDocumentos == totalDocumentosExtranjero - 1:  # porque ya borro antes el que ya existia
        datoUser = User.objects.filter(is_superuser=True, is_staff=True).values_list('id')
        Notificacion.objects.create(titulo='Convocatoria', mensaje='Hay documentos que validar', destinatario=datoUser[0][0], remitente=0)
    if not estudioExtranjero[0][0] and cuentaDocumentos == totalDocumentosNacional - 1:  # porque ya borro antes el que ya existia
        datoUser = User.objects.filter(is_superuser=True, is_staff=True).values_list('id')
        Notificacion.objects.create(titulo='Convocatoria', mensaje='Hay documentos que validar', destinatario=datoUser[0][0], remitente=0)


class DocumentoRevalidacionCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 1)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 1
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCurpCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 2)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 2
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            totalDocumentosNotifica(request)
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoActaNacimientoCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 3)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 3
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            totalDocumentosNotifica(request)
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCartaSolicitudCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 4)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 4
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            totalDocumentosNotifica(request)
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoConstanciaPosgradoCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 5)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 5
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            totalDocumentosNotifica(request)
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCedulaEspecialidadCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 6)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 6
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            totalDocumentosNotifica(request)
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoTituloLicenciaturaCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 7)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 7
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            totalDocumentosNotifica(request)
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCedulaProfesionalCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 8)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 8
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            totalDocumentosNotifica(request)
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoConstanciaCirugiaCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 9)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 9
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            totalDocumentosNotifica(request)
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCartaProfesorCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 10)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 10
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            totalDocumentosNotifica(request)
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoFotoCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 12)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 12
        request.data['engargoladoOk'] = True
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            totalDocumentosNotifica(request)
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentosMedicoListView(ListAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoListSerializer

    def get_queryset(self):
        convocatoriaId = self.kwargs['convocatoriaId']
        medicoId = self.kwargs['medicoId']
        queryset = ConvocatoriaEnroladoDocumento.objects.filter(convocatoria=convocatoriaId, medico=medicoId)
        return queryset


class ConvocatoriaDocumentoUpdateView(UpdateAPIView):
    queryset = ConvocatoriaEnroladoDocumento.objects.filter()
    serializer_class = ConvocatoriaDocumentoSerializer

    def put(self, request, *args, **kwargs):
        datoUser = User.objects.filter(is_superuser=True, is_staff=True).values_list('id')
        Notificacion.objects.create(titulo='Convocatoria', mensaje='Se modificó un documento previamente rechazado', destinatario=datoUser[0][0], remitente=0)
        return self.update(request, *args, **kwargs)


def renderPdfView(request, templateSrc, datosContexto):
    template_path = templateSrc
    context = datosContexto
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ficha-registro.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    ssl._create_default_https_context = ssl._create_unverified_context
    # create a pdf
    pisa_status = pisa.CreatePDF(
        #    html, dest=response, link_callback=link_callback)
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('Error: ' + html)
    return response


class FichaRegistroPDF(View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        try:
            convocatoriaEnrolado = ConvocatoriaEnrolado.objects.get(id=id)
            datos = {
                'id': convocatoriaEnrolado.id,
                'nombre': convocatoriaEnrolado.medico.nombre,
                'apPaterno': convocatoriaEnrolado.medico.apPaterno,
                'apMaterno': convocatoriaEnrolado.medico.apMaterno,
                'hospitalResi': convocatoriaEnrolado.medico.hospitalResi,
                'sede': convocatoriaEnrolado.catSedes.descripcion,
                'tipoExamen': convocatoriaEnrolado.catTiposExamen.descripcion,
                'fechaExamen': convocatoriaEnrolado.convocatoria.fechaExamen,
                'horaExamen': convocatoriaEnrolado.convocatoria.horaExamen,
                'fechaResolucion': convocatoriaEnrolado.convocatoria.fechaResolucion
                # 'fechaResolucion': convocatoriaEnrolado.convocatoria.fechaResolucion.strftime('%d/%b/%Y').upper()
                # 'fechaResolucion': convocatoriaEnrolado.convocatoria.fechaResolucion.strftime('%d %B %Y').upper()
            }

            # ay que contar si existe para permitir el generarla multiples veces
            cuenta = ConvocatoriaEnroladoDocumento.objects.filter(medico=convocatoriaEnrolado.medico, convocatoria=convocatoriaEnrolado.convocatoria, catTiposDocumento_id=11).count()
            if cuenta <= 0:
                # para evitar que se presenten duplicados
                ConvocatoriaEnroladoDocumento.objects.filter(medico=convocatoriaEnrolado.medico, convocatoria=convocatoriaEnrolado.convocatoria, catTiposDocumento_id=11).delete()
                # crea un registro en documentos, porque este no se sube manual
                ConvocatoriaEnroladoDocumento.objects.create(medico=convocatoriaEnrolado.medico, convocatoria=convocatoriaEnrolado.convocatoria, catTiposDocumento_id=11)

            return renderPdfView(request, 'ficha-registro.html', datos)
        except Exception as e:
            return HttpResponse('Error: ' + str(e), content_type='text/plain')


class ConvocatoriaEnroladoMedicoDetailView(RetrieveAPIView):
    serializer_class = ConvocatoriaEnroladoMedicoDetailSerializer
    lookup_field = 'medico'
    lookup_url_kwarg = 'medicoId'

    def get_queryset(self):
        # medicoId = self.kwargs['medicoId']
        # queryset = ConvocatoriaEnrolado.objects.filter(medico=medicoId)
        queryset = ConvocatoriaEnrolado.objects.filter()
        return queryset


def getQuerysetEnroladosMedico(convocatoriaId, isAceptado, nombre, apPaterno):
    if nombre != 'all' and apPaterno != 'all':
        queryset = ConvocatoriaEnrolado.objects.filter(convocatoria=convocatoriaId, isAceptado=isAceptado, medico__nombre__iexact=nombre, medico__apPaterno__iexact=apPaterno)
        return queryset

    if nombre != 'all':
        queryset = ConvocatoriaEnrolado.objects.filter(convocatoria=convocatoriaId, isAceptado=isAceptado, medico__nombre__iexact=nombre)
        return queryset

    if apPaterno != 'all':
        queryset = ConvocatoriaEnrolado.objects.filter(convocatoria=convocatoriaId, isAceptado=isAceptado, medico__apPaterno__iexact=apPaterno)
        return queryset

    queryset = ConvocatoriaEnrolado.objects.filter(convocatoria=convocatoriaId, isAceptado=isAceptado)
    return queryset


class ConvocatoriaEnroladosMedicoListView(ListAPIView):
    serializer_class = ConvocatoriaEnroladosMedicoListSerializer

    def get_queryset(self):
        convocatoriaId = self.kwargs['convocatoriaId']
        isAceptado = self.kwargs['isAceptado']
        if isAceptado == 'true':
            isAceptado = True
        else:
            isAceptado = False
        nombre = self.kwargs['nombre']
        apPaterno = self.kwargs['apPaterno']
        log.info(f'se busca por: convocatoriaId: {convocatoriaId} - isAceptado: {isAceptado} - nombre: {nombre} - apPaterno: {apPaterno}')

        return getQuerysetEnroladosMedico(convocatoriaId, isAceptado, nombre, apPaterno)


class ConvocatoriaEnroladosMedicoEndPoint(APIView):
    def get(self, request, *args, **kwargs):
        convocatoriaId = kwargs['convocatoriaId']
        isAceptado = kwargs['isAceptado']
        if isAceptado == 'true':
            isAceptado = True
        else:
            isAceptado = False
        nombre = kwargs['nombre']
        apPaterno = kwargs['apPaterno']
        log.info(f'se busca por: convocatoriaId: {convocatoriaId} - isAceptado: {isAceptado} - nombre: {nombre} - apPaterno: {apPaterno}')

        queryset = getQuerysetEnroladosMedico(convocatoriaId, isAceptado, nombre, apPaterno)

        size = self.request.query_params.get('size', None)
        direc = self.request.query_params.get('direc', None)
        orderby = self.request.query_params.get('orderby', None)
        page = self.request.query_params.get('page', None)

        paginacion = Paginacion(queryset, ConvocatoriaEnroladosMedicoListSerializer, size, direc, orderby, page)
        serializer = paginacion.paginar()

        respuesta = {
            "totalElements": paginacion.totalElements,
            "totalPages": paginacion.totalPages,
            "sort": paginacion.orderby,
            "direction": paginacion.direc,
            "size": paginacion.size,
            "content": serializer.data
        }
        return Response(respuesta)


class ConvocatoriaEnroladoComentarioUpdateView(UpdateAPIView):
    queryset = ConvocatoriaEnrolado.objects.filter()
    serializer_class = ConvocatoriaEnroladoComentarioSerializer


class ConvocatoriaEnroladoDocumentoAceptarUpdateView(UpdateAPIView):
    queryset = ConvocatoriaEnroladoDocumento.objects.filter()
    serializer_class = ConvocatoriaEnroladoDocumentoAceptarSerializer
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        # para poder modificar el dato que llega
        request.data['isValidado'] = True
        request.data['notasValidado'] = ''
        request.data['rechazoValidado'] = ''

        return self.update(request, *args, **kwargs)


class ConvocatoriaEnroladoDocumentoRechazarUpdateView(UpdateAPIView):
    queryset = ConvocatoriaEnroladoDocumento.objects.filter()
    serializer_class = ConvocatoriaEnroladoDocumentoRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        # para poder modificar el dato que llega
        request.data['isValidado'] = False

        return self.update(request, *args, **kwargs)


class ConvocatoriaEnroladoEngargoladoAceptarUpdateView(UpdateAPIView):
    queryset = ConvocatoriaEnroladoDocumento.objects.filter()
    serializer_class = ConvocatoriaEnroladoEngargoladoAceptarSerializer
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        # para poder modificar el dato que llega
        request.data['engargoladoOk'] = True
        request.data['notasEngargolado'] = ''
        request.data['rechazoEngargolado'] = ''

        return self.update(request, *args, **kwargs)


class ConvocatoriaEnroladoEngargoladoRechazarUpdateView(UpdateAPIView):
    queryset = ConvocatoriaEnroladoDocumento.objects.filter()
    serializer_class = ConvocatoriaEnroladoEngargoladoRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        # para poder modificar el dato que llega
        request.data['engargoladoOk'] = False

        return self.update(request, *args, **kwargs)


class ConvocatoriaEnroladoMedicoAPagarEndPoint(APIView):
    def getQuerySet(self, medicoId, convocatoriaId):
        try:
            return ConvocatoriaEnrolado.objects.get(medico=medicoId, convocatoria=convocatoriaId, isAceptado=True)
        except ConvocatoriaEnrolado.DoesNotExist:
            cuenta = ConvocatoriaEnrolado.objects.filter(medico=medicoId, convocatoria=convocatoriaId).count()
            if cuenta == 1:
                log.info(f'No tiene permitido pagar - convocatoriaId: {convocatoriaId} y medicoId: {medicoId}')
                raise ResponseError(f'No tiene permitido pagar - convocatoriaId: {convocatoriaId} y medicoId: {medicoId}', 409)
            log.info(f'No existe registro - convocatoriaId: {convocatoriaId} y medicoId: {medicoId}')
            raise ResponseError(f'No existe registro con convocatoriaId: {convocatoriaId} y medicoId: {medicoId}', 404)

    def get(self, request, *args, **kwargs):
        convocatoriaId = kwargs['convocatoriaId']
        medicoId = kwargs['medicoId']
        queryset = self.getQuerySet(medicoId, convocatoriaId)
        serializer = ConvocatoriaEnroladoMedicoAPagarDetailSerializer(queryset)
        return Response(serializer.data)


class ConvocatoriaEnroladoMedicoPagadoUpdateView(UpdateAPIView):
    queryset = ConvocatoriaEnrolado.objects.filter()
    serializer_class = ConvocatoriaEnroladoMedicoPagadoSerializer
    # permission_classes = (permissions.IsAdminUser,) # No porque se utiliza desde un usuario normal

    def put(self, request, *args, **kwargs):
        id = kwargs['pk']
        cuenta = ConvocatoriaEnrolado.objects.filter(id=id, isAceptado=True).count()
        if cuenta == 1:
            request.data['isPagado'] = True
            return self.update(request, *args, **kwargs)
        cuenta = ConvocatoriaEnrolado.objects.filter(id=id).count()
        if cuenta == 1:
            raise ResponseError('No tiene permitido pagar', 409)
        raise ResponseError('No existe registro', 404)


def digitalEngargolado(datos, medicoId, convocatoriaId, digEng):
    if digEng == 'digital':
        rechazados = ConvocatoriaEnroladoDocumento.objects.filter(medico=medicoId, convocatoria=convocatoriaId, isValidado=False)
        rechazadosDic = [{'notasValidado': rechazado.notasValidado, 'rechazoValidado': rechazado.rechazoValidado,
                          'documento': rechazado.catTiposDocumento.descripcion} for rechazado in rechazados]
        datos['rechazados'] = rechazadosDic
    else:
        rechazados = ConvocatoriaEnroladoDocumento.objects.filter(medico=medicoId, convocatoria=convocatoriaId, engargoladoOk=False)
        rechazadosDic = [{'notasEngargolado': rechazado.notasEngargolado, 'rechazoEngargolado': rechazado.rechazoEngargolado,
                          'documento': rechazado.catTiposDocumento.descripcion} for rechazado in rechazados]
        datos['rechazados'] = rechazadosDic

    return datos


def preparaDatos(datos, medicoId, convocatoriaId, param, totalDocumentosExtranjero, totalDocumentosNacional):  # param -  Documentos/Engargolado
    estudioExtranjero = datos['estudioExtranjero']
    cuentaDocumentos = datos['cuentaDocumentos']
    if param == 'Engargolado':  # tiene un documento extra el cual es la ficha de registro que se genera al descargarla
        totalDocumentosExtranjero = totalDocumentosExtranjero + 1
        totalDocumentosNacional = totalDocumentosNacional + 1
    if estudioExtranjero:
        if cuentaDocumentos == totalDocumentosExtranjero:
            datos['mensaje'] = 'correo enviado a medico estudio extranjero con todos sus documentos validados'
            datos['aceptado'] = True
            datos['titulo'] = f'CMCPER - Validación de {param} - OK'
            return datos
        datos['mensaje'] = 'correo enviado a medico estudio extranjero con documentos faltantes'
        datos['aceptado'] = False
        datos['titulo'] = f'CMCPER - Validación de {param} - Rechazado'
        if param == 'Documentos':
            digitalEngargolado(datos, medicoId, convocatoriaId, 'digital')
        else:
            digitalEngargolado(datos, medicoId, convocatoriaId, 'no digital')
        return datos
    else:
        if cuentaDocumentos == totalDocumentosNacional:
            datos['mensaje'] = 'correo enviado a medico con todos sus documentos validados'
            datos['aceptado'] = True
            datos['titulo'] = f'CMCPER - Validación de {param} - OK'
            return datos
        datos['mensaje'] = 'correo enviado a medico documentos faltantes'
        datos['aceptado'] = False
        datos['titulo'] = f'CMCPER - Validación de {param} - Rechazado'
        if param == 'Documentos':
            digitalEngargolado(datos, medicoId, convocatoriaId, 'digital')
        else:
            digitalEngargolado(datos, medicoId, convocatoriaId, 'no digital')
        return datos


class CorreoEngargoladoEndPoint(APIView):
    def get(self, request, *args, **kwargs):
        convocatoriaId = kwargs['convocatoriaId']
        medicoId = kwargs['medicoId']
        cuentaDocumentos = ConvocatoriaEnroladoDocumento.objects.filter(medico=medicoId, convocatoria=convocatoriaId, engargoladoOk=True).count()
        # cuentaMedico = Medico.objects.filter(id=medicoId, estudioExtranjero=True).count()
        datosMedico = Medico.objects.filter(id=medicoId).values_list('nombre', 'apPaterno', 'apMaterno', 'email', 'estudioExtranjero')
        datos = {
            'nombre': datosMedico[0][0],
            'apPaterno': datosMedico[0][1],
            'estudioExtranjero': datosMedico[0][4],
            'email': datosMedico[0][3],
            'cuentaDocumentos': cuentaDocumentos,  # fines de control
            # 'cuentaMedico': cuentaMedico # fines de control
        }
        preparaDatos(datos, medicoId, convocatoriaId, 'Engargolado', totalDocumentosExtranjero, totalDocumentosNacional)
        ConvocatoriaEnrolado.objects.filter(medico=medicoId, convocatoria=convocatoriaId).update(isAceptado=datos['aceptado'])  # setteado para que pueda pagar o no
        try:
            htmlContent = render_to_string('engar-a-r.html', datos)
            textContent = strip_tags(htmlContent)
            emailAcep = EmailMultiAlternatives(datos['titulo'], textContent, "no-reply@cmcper.mx", [datos['email']])
            emailAcep.attach_alternative(htmlContent, "text/html")
            emailAcep.send()
        except:
            raise ResponseError('Error al enviar correo', 500)

        return Response(datos)


class CorreoDocumentosEndPoint(APIView):
    def get(self, request, *args, **kwargs):
        convocatoriaId = kwargs['convocatoriaId']
        medicoId = kwargs['medicoId']
        cuentaDocumentos = ConvocatoriaEnroladoDocumento.objects.filter(medico=medicoId, convocatoria=convocatoriaId, isValidado=True).count()
        # cuentaMedico = Medico.objects.filter(id=medicoId, estudioExtranjero=True).count()
        datosMedico = Medico.objects.filter(id=medicoId).values_list('nombre', 'apPaterno', 'apMaterno', 'email', 'estudioExtranjero')
        datos = {
            'nombre': datosMedico[0][0],
            'apPaterno': datosMedico[0][1],
            'estudioExtranjero': datosMedico[0][4],
            'email': datosMedico[0][3],
            'cuentaDocumentos': cuentaDocumentos,  # fines de control
            # 'cuentaMedico': cuentaMedico # fines de control
        }
        preparaDatos(datos, medicoId, convocatoriaId, 'Documentos', totalDocumentosExtranjero, totalDocumentosNacional)
        try:
            htmlContent = render_to_string('doc-dig-a-r.html', datos)
            textContent = strip_tags(htmlContent)
            emailAcep = EmailMultiAlternatives(datos['titulo'], textContent, "no-reply@cmcper.mx", [datos['email']])
            emailAcep.attach_alternative(htmlContent, "text/html")
            emailAcep.send()
        except:
            raise ResponseError('Error al enviar correo', 500)

        return Response(datos)


class ConvocatoriaEnroladosExcelListView(ListAPIView):
    serializer_class = ConvocatoriaEnroladosMedicoListSerializer

    def get_queryset(self):
        convocatoriaId = self.kwargs['convocatoriaId']
        queryset = ConvocatoriaEnrolado.objects.filter(convocatoria=convocatoriaId)

        return queryset


def renderCsvView(request, queryset):
    response = HttpResponse(content_type='text/csv')
    # response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="calificaciones-medicos.csv"'
    writer = csv.writer(response)
    writer.writerow(['NO TOCAR', 'Num. de Registro', 'Nombre', 'Apellido Paterno', 'Apellido Materno', 'Calificacion', 'Aprobado'])
    for dato in queryset:
        writer.writerow(dato)

    return response


class ConvocatoriaEnroladosDownExcel(View):
    def get(self, request, *args, **kwargs):
        convocatoriaId = self.kwargs['convocatoriaId']
        try:
            queryset = ConvocatoriaEnrolado.objects.filter(convocatoria=convocatoriaId).values_list('id', 'medico__numRegistro', 'medico__nombre', 'medico__apPaterno', 'medico__apMaterno',
                                                                                                    'calificacion', 'isAprobado')
            # print(f'--->>>queryset como tupla(values_list): {queryset}')
            if not queryset:
                respuesta = {"detail": "Registros no encontrados"}
                return Response(respuesta, status=status.HTTP_404_NOT_FOUND)

            return renderCsvView(request, queryset)
        except Exception as e:
            respuesta = {"detail": str(e)}
            return Response(respuesta, status=status.HTTP_409_CONFLICT)


class ConvocatoriaAprobadosDownExcel(View):
    def get(self, request, *args, **kwargs):
        convocatoriaId = self.kwargs['convocatoriaId']
        try:
            queryset = ConvocatoriaEnrolado.objects.filter(convocatoria=convocatoriaId, isAprobado=True).values_list(
                'id', 'medico__numRegistro', 'medico__nombre', 'medico__apPaterno', 'medico__apMaterno', 'calificacion', 'isAprobado')
            # print(f'--->>>queryset como tupla(values_list): {queryset}')
            if not queryset:
                respuesta = {"detail": "Registros no encontrados"}
                return Response(respuesta, status=status.HTTP_404_NOT_FOUND)

            return renderCsvView(request, queryset)
        except Exception as e:
            respuesta = {"detail": str(e)}
            return Response(respuesta, status=status.HTTP_409_CONFLICT)


class ConvocatoriaEnroladosUpExcel(APIView):
    def put(self, request, *args, **kwargs):
        # archivo = request.FILES['archivo']
        archivo = request.data['archivo']
        datosList = list(csv.reader(codecs.iterdecode(archivo, 'utf-8'), delimiter=','))
        datosList.pop(0)
        try:
            for row in datosList:
                ConvocatoriaEnrolado.objects.filter(id=row[0]).update(calificacion=row[5], isAprobado=row[6])
            respuesta = {"detail": "Datos subidos correctamente"}
            return Response(respuesta, status=status.HTTP_200_OK)
        except Exception as e:
            respuesta = {"detail": str(e)}
            return Response(respuesta, status=status.HTTP_409_CONFLICT)


class SubirPagoCreateView(CreateAPIView):
    serializer_class = ConvocatoriaPagoSerializer

    def post(self, request, *args, **kwargs):
        request.data['estatus'] = 3
        serializer = ConvocatoriaPagoSerializer(data=request.data)
        if serializer.is_valid():
            datoUser = User.objects.filter(is_superuser=True, is_staff=True).values_list('id')
            Notificacion.objects.create(titulo='Convocatoria', mensaje='Se subió un pago', destinatario=datoUser[0][0], remitente=0)
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


def getQuerysetEstatus(estatus):
    if estatus == 0:
        queryset = Pago.objects.all()
        return queryset

    queryset = Pago.objects.filter(estatus=estatus)
    return queryset


class PagosListView(ListAPIView):
    serializer_class = PagosListSerializer

    def get_queryset(self):
        estatus = self.kwargs['estatus']
        log.info(f'se busca por: estatus: {estatus}')

        return getQuerysetEstatus(estatus)


class PagoAceptarUpdateView(UpdateAPIView):
    queryset = Pago.objects.filter()
    serializer_class = PagoAceptarRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        id = kwargs['pk']
        try:
            dato = Pago.objects.get(id=id)
        except Exception as e:
            raise ResponseError('No existe registro', 404)

        cuenta = ConvocatoriaEnrolado.objects.filter(id=dato.convocatoriaEnrolado.id, isAceptado=True).count()
        if cuenta == 1:
            request.data['estatus'] = 1
            ConvocatoriaEnrolado.objects.filter(id=dato.convocatoriaEnrolado.id).update(isPagado=True)
            return self.update(request, *args, **kwargs)
        cuenta = ConvocatoriaEnrolado.objects.filter(id=dato.convocatoriaEnrolado.id).count()
        if cuenta == 1:
            raise ResponseError('No tiene permitido pagar', 409)


class PagoRechazarUpdateView(UpdateAPIView):
    queryset = Pago.objects.filter()
    serializer_class = PagoAceptarRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        id = kwargs['pk']
        try:
            dato = Pago.objects.get(id=id)
        except Exception as e:
            raise ResponseError('No existe registro', 404)

        cuenta = ConvocatoriaEnrolado.objects.filter(id=dato.convocatoriaEnrolado.id, isAceptado=True).count()
        if cuenta == 1:
            request.data['estatus'] = 2
            ConvocatoriaEnrolado.objects.filter(id=dato.convocatoriaEnrolado.id).update(isPagado=False)
            return self.update(request, *args, **kwargs)
        cuenta = ConvocatoriaEnrolado.objects.filter(id=dato.convocatoriaEnrolado.id).count()
        if cuenta == 1:
            raise ResponseError('No tiene permitido pagar', 409)


class PublicarCalificaciones(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, *args, **kwargs):
        convocatoriaId = self.kwargs['convocatoriaId']
        try:
            queryset = ConvocatoriaEnrolado.objects.filter(convocatoria=convocatoriaId).values_list('id', 'medico__numRegistro', 'medico__nombre', 'medico__apPaterno', 'medico__apMaterno',
                                                                                                    'convocatoria__fechaExamen', 'calificacion', 'medico__email', 'isAprobado', 'medico__id',
                                                                                                    'isPublicado')
            # print(f'--->>>queryset como tupla(values_list): {queryset}')
            if not queryset:
                respuesta = {"detail": "Registros no encontrados"}
                return Response(respuesta, status=status.HTTP_404_NOT_FOUND)

            for dato in queryset:
                if dato[8] and not dato[10]:  # se checa que este aprobado y no publicado
                    # hay que crear un nuevo campo de isPublicado y con ese verificar si se crea o no un certificado nuevo
                    medico = Medico.objects.get(id=dato[9])
                    Certificado.objects.create(medico=medico, documento='', descripcion='generado automaticamente por convocatoria', isVencido=False, estatus=1)
                    ConvocatoriaEnrolado.objects.filter(medico=dato[9]).update(isPublicado=True)

                datos = {
                    'nombre': dato[2],
                    'apPaterno': dato[3],
                    'apMaterno': dato[4],
                    'fechaExamen': dato[5],
                    'anioExamen': dato[5].strftime("%Y"),
                    # 'aceptado': True if dato[6] > 5 else False,
                    'aceptado': dato[8],
                    'email': dato[7]
                }
                # print(f'--->>>datos: {datos}')
                try:
                    htmlContent = render_to_string('exam-a-r.html', datos)
                    textContent = strip_tags(htmlContent)
                    emailAcep = EmailMultiAlternatives('CMCPER - Resultado de Examen', textContent, "no-reply@cmcper.mx", [datos['email']])
                    emailAcep.attach_alternative(htmlContent, "text/html")
                    emailAcep.send()
                except:
                    raise ResponseError('Error al enviar correo', 500)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            respuesta = {"detail": str(e)}
            return Response(respuesta, status=status.HTTP_409_CONFLICT)


# ES DE PRUEBA NO USAR!!!

# https://www.django-rest-framework.org/api-guide/filtering/
# class prueba(ListAPIView):
#     queryset = ConvocatoriaEnrolado.objects.filter()
#     serializer_class = ConvocatoriaEnroladosMedicoListSerializer
#     filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
#     filter_fields = ('medico', 'convocatoria')

# class ConvocatoriaSedeCreateView(CreateAPIView):
#     def post(self, request, *args, **kwargs):
#         print(f'--->>>reques.data: {request.data}')
#         print(f'--->>>reques.data: {type(request.data)}')
#         # lista =  list(request.POST.getlist('catSedes'))
#         lista = list(request.data.get('catSedes'))
#         # print(f'--->>>asd: {type(lista)}')
#         # print(f'--->>>lista: {lista}')
#         convocatoriaId = self.kwargs['convocatoriaId']
#         # print(f'--->>>kwargs: {convocatoriaId}')
#         convocatoria = Convocatoria.objects.get(id=convocatoriaId)
#         Sede.objects.filter(convocatoria=convocatoria).delete()
#         for dato in lista:
#             print(dato)
#             catSedes = CatSedes.objects.get(id=dato)
#             Sede.objects.create(catSedes=catSedes, convocatoria=convocatoria)
#         # return JsonResponse({"ok":"ok"}, status=status.HTTP_201_CREATED)
#         return Response({"ok":"ok"}, status=status.HTTP_201_CREATED)
