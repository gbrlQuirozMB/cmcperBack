from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from preregistro.models import Medico

# from api.logger import log
import logging
log = logging.getLogger('django')
from api.exceptions import *

from .serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status, permissions

from datetime import date
from dateutil.relativedelta import relativedelta

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from rest_framework.views import APIView

from notificaciones.models import Notificacion
from django.contrib.auth.models import User

from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
# from django_filters import rest_framework as filters

from django.http import HttpResponse
from django.views import View

import csv
import codecs

from certificados.models import Certificado
from actividadesAvaladas.models import AsistenteActividadAvalada, ActividadAvalada

# Create your views here.
# class CertificadoDatosDetailView(RetrieveAPIView):
#     serializer_class = CertificadoDatosSerializer
#     lookup_field = 'medico'
#     lookup_url_kwarg = 'medicoId'

#     def get_queryset(self):
#         # queryset = Certificado.objects.filter(isVencido=False)
#         # queryset = Certificado.objects.filter(estatus=1)
#         # queryset = Certificado.objects.order_by('-actualizado_en')[0]
#         queryset = Certificado.objects.filter()
#         return queryset


class CertificadoDatosDetailView(RetrieveAPIView):
    serializer_class = CertificadoDatosSerializer
    
    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        try:
            queryset = Certificado.objects.filter(medico=medicoId)[0]
            serializer = CertificadoDatosSerializer(queryset)
        except:
            raise ResponseError('No hay certificado para el ID de Medico dado', 404)

        return Response(serializer.data)


class AvanceMedicoCapituloDetailView(RetrieveAPIView):
    serializer_class = AvanceMedicoCapituloSerializer

    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        capituloId = kwargs['capituloId']
        try:
            datosCapitulo = Capitulo.objects.get(id=capituloId)
            queryset = RecertificacionItemDocumento.objects.filter(medico=medicoId, item__subcapitulo__capitulo=capituloId, estatus=1).aggregate(Sum('puntosOtorgados'))
            if queryset['puntosOtorgados__sum'] is None:
                raise ResponseError('Médico no ecnontrado', 404)
            puntosOtorgados = queryset['puntosOtorgados__sum']
            avance = round(puntosOtorgados * 100 / datosCapitulo.puntos, 2)
            avanceMedicoCapitulo = AvanceMedicoCapitulo(datosCapitulo.descripcion, datosCapitulo.puntos, puntosOtorgados, avance)
            serializer = AvanceMedicoCapituloSerializer(avanceMedicoCapitulo)
            # return Response(JSONRenderer().render(serializer.data))
            return Response(serializer.data)
        except Capitulo.DoesNotExist:
            raise ResponseError('Capítulo no encontrado', 404)


class PuntosCapituloListView(ListAPIView):
    queryset = Capitulo.objects.all().order_by('id')
    serializer_class = PuntosCapituloListSerializer


class PuntosCapituloDetailView(RetrieveAPIView):
    queryset = Capitulo.objects.filter()
    serializer_class = PuntosCapituloDetailSerializer


class PorcentajeGeneralMedicoDetailView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        try:
            datosMedico = Medico.objects.get(id=medicoId)
            querysetPAR = Capitulo.objects.aggregate(Sum('puntos'))
            if querysetPAR['puntos__sum'] is None:
                raise ResponseError('No hay capítulos', 404)
            puntosAReunir = querysetPAR['puntos__sum']
            querysetPO = RecertificacionItemDocumento.objects.filter(medico=medicoId, estatus=1).aggregate(Sum('puntosOtorgados'))
            if querysetPO['puntosOtorgados__sum'] is None:
                raise ResponseError('No hay documentos', 404)
            puntosObtenidos = querysetPO['puntosOtorgados__sum']
            porcentaje = round(puntosObtenidos * 100 / puntosAReunir, 2)
            nombreCompleto = datosMedico.nombre + ' ' + datosMedico.apPaterno + ' ' + datosMedico.apMaterno
            porcentageGeneralMedico = PorcentajeGeneralMedico(nombreCompleto, datosMedico.numRegistro, porcentaje, puntosObtenidos, puntosAReunir)
            serializer = PorcentajeGeneralMedicoSerializer(porcentageGeneralMedico)
            return Response(serializer.data)
        except Medico.DoesNotExist:
            raise ResponseError('Médico no encontrado', 404)


class PuntosPorCapituloMedicoDetailView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        capituloId = kwargs['capituloId']
        try:
            queryset = Capitulo.objects.get(id=capituloId)
            puntos = queryset.puntos
            querysetPO = RecertificacionItemDocumento.objects.filter(medico=medicoId, item__subcapitulo__capitulo=capituloId, estatus=1).aggregate(Sum('puntosOtorgados'))
            if querysetPO['puntosOtorgados__sum'] is None:
                raise ResponseError('Médico no encontrado', 404)
            reunidos = querysetPO['puntosOtorgados__sum']
            isExcedido = True if reunidos > puntos else False
            faltantes = round(puntos - reunidos, 2) if not isExcedido else 0
            excedentes = abs(round(puntos - reunidos, 2)) if isExcedido else 0
            puntosPorCapituloMedico = PuntosPorCapituloMedico(queryset.titulo, queryset.descripcion, reunidos, faltantes, isExcedido, excedentes, puntos)
            serializer = PuntosPorCapituloMedicoSerializer(puntosPorCapituloMedico)
            return Response(serializer.data)
        except Capitulo.DoesNotExist:
            raise ResponseError('Capítulo no encontrado', 404)


class DetallesCapituloDetailView(RetrieveAPIView):
    queryset = Capitulo.objects.filter()
    serializer_class = DetallesCapituloSerializer


class ItemDocumentosListView(ListAPIView):
    serializer_class = ItemDocumentosSerializer

    def get_queryset(self):
        itemId = self.kwargs['itemId']
        medicoId = self.kwargs['medicoId']
        queryset = RecertificacionItemDocumento.objects.filter(item=itemId, medico=medicoId)
        if not queryset:
            raise ResponseError('No hay documentos', 404)
        # print(f'--->>>queryset: {queryset is None}')
        # print(f'--->>>queryset: {not queryset}')
        return queryset


class ItemDocumentosCreateView(CreateAPIView):
    serializer_class = ItemDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request.data['estatus'] = 3
        request.data['puntosOtorgados'] = 0
        request.data['observaciones'] = ''
        request.data['notasRechazo'] = ''
        request.data['razonRechazo'] = ''
        serializer = ItemDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class CertificadosMedicoListView(ListAPIView):
    serializer_class = CertificadosMedicoListSerialializer

    def get_queryset(self):
        medicoId = self.kwargs['medicoId']
        queryset = Certificado.objects.filter(medico=medicoId)
        if not queryset:
            raise ResponseError('No hay certificados', 404)
        return queryset


def getQuerysetItemDocumentosFiltered(estatus, nombre, apPaterno):
    # queryset = RecertificacionItemDocumento.objects.filter(estatus=estatus, medico__nombre__iexact=nombre, medico__apPaterno__iexact=apPaterno)
    if nombre == 'all' and apPaterno == 'all' and estatus == '0':
        queryset = RecertificacionItemDocumento.objects.filter()
        return queryset

    if nombre == 'all' and apPaterno == 'all' and estatus != '0':
        queryset = RecertificacionItemDocumento.objects.filter(estatus=estatus)
        return queryset

    if nombre == 'all' and apPaterno != 'all' and estatus == '0':
        queryset = RecertificacionItemDocumento.objects.filter(medico__apPaterno__iexact=apPaterno)
        return queryset

    if nombre == 'all' and apPaterno != 'all' and estatus != '0':
        queryset = RecertificacionItemDocumento.objects.filter(medico__apPaterno__iexact=apPaterno, estatus=estatus)
        return queryset

    if nombre != 'all' and apPaterno == 'all' and estatus == '0':
        queryset = RecertificacionItemDocumento.objects.filter(medico__nombre__iexact=nombre)
        return queryset

    if nombre != 'all' and apPaterno == 'all' and estatus != '0':
        queryset = RecertificacionItemDocumento.objects.filter(medico__nombre__iexact=nombre, estatus=estatus)
        return queryset

    if nombre != 'all' and apPaterno != 'all' and estatus == '0':
        queryset = RecertificacionItemDocumento.objects.filter(medico__nombre__iexact=nombre, medico__apPaterno__iexact=apPaterno)
        return queryset

    if nombre != 'all' and apPaterno != 'all' and estatus != '0':
        queryset = RecertificacionItemDocumento.objects.filter(medico__nombre__iexact=nombre, medico__apPaterno__iexact=apPaterno, estatus=estatus)
        return queryset


class ItemDocumentosFilteredListView(ListAPIView):
    serializer_class = ItemDocumentoFilteredSerializer

    def get_queryset(self):
        estatus = self.kwargs['estatus']
        nombre = self.kwargs['nombre']
        apPaterno = self.kwargs['apPaterno']
        # log.error(f'--->>>se busca por:  estatus: {estatus} - nombre: {nombre} - apPaterno: {apPaterno}')

        return getQuerysetItemDocumentosFiltered(estatus, nombre, apPaterno)


class ItemDocumentosDetailView(RetrieveAPIView):
    queryset = RecertificacionItemDocumento.objects.filter()
    serializer_class = ItemDocumentoDetailSerializer


class ItemDocumentosAceptar(UpdateAPIView):
    queryset = RecertificacionItemDocumento.objects.filter()
    serializer_class = ItemDocumentoAceptarRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        request.data['estatus'] = 1
        request.data['notasRechazo'] = ''
        request.data['razonRechazo'] = ''

        return self.update(request, *args, **kwargs)


class ItemDocumentosRechazar(UpdateAPIView):
    queryset = RecertificacionItemDocumento.objects.filter()
    serializer_class = ItemDocumentoAceptarRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        request.data['estatus'] = 2
        request.data['puntosOtorgados'] = 0

        return self.update(request, *args, **kwargs)


class ItemDocumentosReasignar(UpdateAPIView):
    queryset = RecertificacionItemDocumento.objects.filter()
    serializer_class = ItemDocumentoReasignarSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        request.data['estatus'] = 1
        request.data['notasRechazo'] = ''
        request.data['razonRechazo'] = ''

        return self.update(request, *args, **kwargs)


class CapituloListView(ListAPIView):
    queryset = Capitulo.objects.all()
    serializer_class = CapituloListSerializer


class CapituloUpdateView(UpdateAPIView):
    queryset = Capitulo.objects.filter()
    serializer_class = CapituloSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']


class SubcapituloListView(ListAPIView):
    serializer_class = SubcapituloListSerializer

    def get_queryset(self):
        capituloId = self.kwargs['capituloId']
        queryset = Subcapitulo.objects.filter(capitulo=capituloId)
        if not queryset:
            raise ResponseError('No existen subcapitulos con el capituloId proporcionado', 404)
        return queryset


class SubcapituloUpdateView(UpdateAPIView):
    queryset = Subcapitulo.objects.filter()
    serializer_class = SubcapituloUpdateSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']


class SubcapituloDetailView(RetrieveAPIView):
    queryset = Subcapitulo.objects.filter()
    serializer_class = DetallesSubcapituloSerializer


class ItemListView(ListAPIView):
    serializer_class = ItemListSerializer

    def get_queryset(self):
        subcapituloId = self.kwargs['subcapituloId']
        queryset = Item.objects.filter(subcapitulo=subcapituloId)
        if not queryset:
            raise ResponseError('No existen items con el subcapituloId proporcionado', 404)
        return queryset


class ItemUpdateView(UpdateAPIView):
    queryset = Item.objects.filter()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']


class ItemDetailView(RetrieveAPIView):
    queryset = Item.objects.filter()
    serializer_class = ItemSerializer


class ActualizaVigenciaCertificados(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        try:
            # para quitarle al medico su certificacion
            itemIds = []
            for dato in Certificado.objects.filter(isVencido=False, fechaCaducidad__lt=date.today()):
                if dato.medico.id not in itemIds:
                    itemIds.append(dato.medico.id)
            Medico.objects.filter(pk__in=itemIds).update(isCertificado=False)
            # print(f'--->>>itemIds: {itemIds}')
            
            cuentaVencidos = Certificado.objects.filter(isVencido=False, fechaCaducidad__lt=date.today()).update(estatus=3, isVencido=True)
            cuentaVigentes = Certificado.objects.filter(isVencido=False, fechaCaducidad__gte=date.today()).update(estatus=1, isVencido=False)
            cuentaPorVencer = Certificado.objects.filter(isVencido=False, fechaCaducidad__range=[date.today(), date.today()+relativedelta(years=1)]).update(estatus=2, isVencido=False)

            respuesta = {
                "cuentaVencidos": cuentaVencidos,
                "cuentaVigentes": cuentaVigentes,
                "cuentaPorVencer": cuentaPorVencer
            }
            return Response(respuesta, status=status.HTTP_200_OK)
        except Exception as e:
            # respuesta = {"detail": str(e)}
            # return Response(respuesta, status=status.HTTP_409_CONFLICT)
            raise ResponseError(f'Error grave: {str(e)}, 409')


class SolicitudExamenCreateView(CreateAPIView):
    serializer_class = SolicitudExamenSerializer

    def post(self, request, *args, **kwargs):
        request.data['estatus'] = 3
        request.data['isAprobado'] = False
        request.data['calificacion'] = 0
        serializer = SolicitudExamenSerializer(data=request.data)
        if serializer.is_valid():
            medicoId = request.data.get('medico')
            cuenta = PorExamen.objects.filter(medico=medicoId, isAprobado=False).count()
            if cuenta > 0:
                dato = PorExamen.objects.filter(medico=medicoId, isAprobado=False).values_list('id')
                # print(f'--->>>dato: {dato[0][0]}')
                jsonRespuesta = {
                    'detail': 'El medico tiene una solicitud de examen pendiente',
                    'porExamenId': dato[0][0]
                }
                # raise ResponseError('El medico tiene una solicitud de examen pendiente', 409)
                raise ResponseError(jsonRespuesta, 409)
            datosMedico = Medico.objects.filter(id=medicoId).values_list('nombre', 'apPaterno', 'apMaterno', 'email')
            queryset = FechasExamenRecertificacion.objects.filter(fechaExamen__gte=date.today())
            if not queryset:
                raise ResponseError('No existe una fecha de examen', 404)
            queryset = queryset.order_by('fechaExamen')[:1]
            request.data['fechaExamen'] = queryset[0].id
            datos = {
                'nombre': datosMedico[0][0],
                'apPaterno': datosMedico[0][1],
                'email': datosMedico[0][3],
                'fechaExamen': queryset[0].fechaExamen
            }
            try:
                htmlContent = render_to_string('cert-vig-exam.html', datos)
                textContent = strip_tags(htmlContent)
                emailAcep = EmailMultiAlternatives('CMCPER - Solicitud de Certificacón Vigente por Examen', textContent, "no-reply@cmcper.mx", [datos['email']])
                emailAcep.attach_alternative(htmlContent, "text/html")
                emailAcep.send()
            except:
                raise ResponseError('Error al enviar correo', 500)

            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


def inicializaData(request):
    request.data['isAceptado'] = False
    return request


def borraExistentes(request, tipoDocumento):
    porExamenId = request.data['porExamen']
    PorExamenDocumento.objects.filter(porExamen=porExamenId, catTiposDocumento=tipoDocumento).delete()


def totalDocumentosNotifica(request):
    porExamenId = request.data['porExamen']
    cuentaDocumentos = PorExamenDocumento.objects.filter(porExamen=porExamenId).count()
    if cuentaDocumentos == 4:  # porque ya borro antes el que ya existia
        datoUser = User.objects.filter(is_superuser=True, is_staff=True).values_list('id')
        Notificacion.objects.create(titulo='Recertificación', mensaje='Hay documentos que validar', destinatario=datoUser[0][0], remitente=0)


class DocumentoCedulaEspecialidadCreateView(CreateAPIView):
    serializer_class = PorExamenDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 6)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 6
        serializer = PorExamenDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            totalDocumentosNotifica(request)
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCertificadoCreateView(CreateAPIView):
    serializer_class = PorExamenDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 13)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 13
        serializer = PorExamenDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            totalDocumentosNotifica(request)
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoFotoCreateView(CreateAPIView):
    serializer_class = PorExamenDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 12)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 12
        serializer = PorExamenDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            porExamenId = request.data.get('porExamen')
            catTiposDocumento = CatTiposDocumento.objects.get(id=14)
            porExamen = PorExamen.objects.get(id=porExamenId)
            borraExistentes(request, 14)
            PorExamenDocumento.objects.create(catTiposDocumento=catTiposDocumento, porExamen=porExamen)
            totalDocumentosNotifica(request)
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCartaSolicitudCreateView(CreateAPIView):
    serializer_class = PorExamenDocumentoSerializer

    def post(self, request, *args, **kwargs):
        borraExistentes(request, 4)
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 4
        serializer = PorExamenDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            totalDocumentosNotifica(request)
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class PorExamenAPagarEndPoint(APIView):
    def getQuerySet(self, medicoId):
        try:
            cuenta = PorExamen.objects.filter(medico=medicoId, isAceptado=True).count()
            if cuenta == 1:
                return CatPagos.objects.get(id=1)
            raise ResponseError('No tiene permitido pagar', 409)
        except CatPagos.DoesNotExist:
            raise ResponseError('No existe un registro de pago para el Examen Certificación Vigente', 404)

    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        cuenta = Medico.objects.filter(id=medicoId).count()
        if cuenta < 1:
            raise ResponseError('No existe medico', 404)
        queryset = self.getQuerySet(medicoId)
        serializer = MedicoAPagarExamenSerializer(queryset, context={'medicoId': medicoId})  # enviamos variable extra para consulta interna en serializer
        return Response(serializer.data)


class RenovacionAPagarEndPoint(APIView):
    def getQuerySet(self):
        try:
            return CatPagos.objects.get(id=6)
        except CatPagos.DoesNotExist:
            raise ResponseError('No existe un registro de pago para Renovación de Certificación', 404)

    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        cuenta = Medico.objects.filter(id=medicoId).count()
        if cuenta < 1:
            raise ResponseError('No existe medico', 404)
        queryset = self.getQuerySet()
        serializer = MedicoAPagarRenovacionSerializer(queryset, context={'medicoId': medicoId})  # enviamos variable extra para consulta interna en serializer
        return Response(serializer.data)


class PorExamenPagadoUpdateView(UpdateAPIView):
    queryset = PorExamen.objects.filter()
    serializer_class = PorExamenPagadoSerializer
    # permission_classes = (permissions.IsAdminUser,) # No porque se utiliza desde un usuario normal
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        id = kwargs['pk']
        cuenta = PorExamen.objects.filter(id=id, isAceptado=True).count()
        if cuenta == 1:
            request.data['isPagado'] = True
            return self.update(request, *args, **kwargs)
        cuenta = PorExamen.objects.filter(id=id).count()
        if cuenta == 1:
            raise ResponseError('No tiene permitido pagar', 409)
        raise ResponseError('No existe registro', 404)


class RenovacionPagadoCreateView(CreateAPIView):
    serializer_class = CertificadoPagadoSerializer

    def post(self, request, *args, **kwargs):
        request.data['estatus'] = 1
        request.data['descripcion'] = 'generado automaticamente por renovacion de recertificacion'
        request.data['isVencido'] = False
        serializer = CertificadoPagadoSerializer(data=request.data)
        if serializer.is_valid():
            RecertificacionItemDocumento.objects.filter(medico=request.data['medico']).delete()
            Medico.objects.filter(id=request.data['medico']).update(isCertificado=True) # una vez que paga el medico pasa a ser certificado
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class PorExamenFilter(FilterSet):
    nombreNS = CharFilter(field_name='medico__nombre', lookup_expr='iexact')
    apPaternoNS = CharFilter(field_name='medico__apPaterno', lookup_expr='iexact')

    class Meta:
        model = PorExamen
        fields = ['nombreNS', 'apPaternoNS', 'estatus', 'fechaExamen']


class PorExamenFilteredListView(ListAPIView):
    queryset = PorExamen.objects.all()
    serializer_class = PorExamenFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PorExamenFilter


class PorExamenDocumentosListView(ListAPIView):
    serializer_class = PorExamenDocumentoSerializer

    def get_queryset(self):
        porExamenId = self.kwargs['porExamenId']
        queryset = PorExamenDocumento.objects.filter(porExamen=porExamenId)
        if not queryset:
            raise ResponseError('No existen documentos con el porExamenId proporcionado', 404)
        return queryset


class PorExamenDocumentoAceptarUpdateView(UpdateAPIView):
    queryset = PorExamenDocumento.objects.filter()
    serializer_class = PorExamenDocumentoAceptarRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        request.data['isAceptado'] = True

        return self.update(request, *args, **kwargs)


class PorExamenDocumentoRechazarUpdateView(UpdateAPIView):
    queryset = PorExamenDocumento.objects.filter()
    serializer_class = PorExamenDocumentoAceptarRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        request.data['isAceptado'] = False

        return self.update(request, *args, **kwargs)


class PorExamenMedicoDetailView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        try:
            # queryset = PorExamen.objects.filter(medico=medicoId, isAprobado=False, isPagado=False, isAceptado=False)[0]
            queryset = PorExamen.objects.filter(medico=medicoId, isAprobado=False)[0]
            serializer = PorExamenMedicoSerializer(queryset)
        except:
            raise ResponseError('No hay solicitud de examen para el ID de Medico dado', 404)

        return Response(serializer.data)


def renderCsvView(request, queryset):
    response = HttpResponse(content_type='text/csv')
    # response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="calificaciones-medicos.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['NO TOCAR', 'Num. de Registro', 'Nombre', 'Apellido Paterno', 'Apellido Materno', 'Calificacion', 'Aprobado'])
    for dato in queryset:
        writer.writerow(dato)
        # writer.writerow(dato.encode('UTF-8'))

    return response


class PorExamenFechaDownExcel(View):
    def get(self, request, *args, **kwargs):
        fechaExamenId = self.kwargs['fechaExamenId']
        try:
            queryset = PorExamen.objects.filter(fechaExamen=fechaExamenId).values_list('id', 'medico__numRegistro', 'medico__nombre', 'medico__apPaterno', 'medico__apMaterno',
                                                                                       'calificacion', 'isAprobado')
            # print(f'--->>>queryset como tupla(values_list): {queryset}')
            if not queryset:
                respuesta = {"detail": "Registros no encontrados"}
                return Response(respuesta, status=status.HTTP_404_NOT_FOUND)

            return renderCsvView(request, queryset)
        except Exception as e:
            respuesta = {"detail": str(e)}
            return Response(respuesta, status=status.HTTP_409_CONFLICT)


class PorExamenFechaUpExcel(APIView):
    def put(self, request, *args, **kwargs):
        # archivo = request.FILES['archivo']
        archivo = request.data['archivo']
        datosList = list(csv.reader(codecs.iterdecode(archivo, 'utf-8'), delimiter=','))
        datosList.pop(0)
        try:
            for row in datosList:
                PorExamen.objects.filter(id=row[0]).update(calificacion=row[5], isAprobado=row[6])
            respuesta = {"detail": "Datos subidos correctamente"}
            return Response(respuesta, status=status.HTTP_200_OK)
        except Exception as e:
            respuesta = {"detail": str(e)}
            return Response(respuesta, status=status.HTTP_409_CONFLICT)


class PublicarCalificaciones(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, *args, **kwargs):
        fechaExamenId = self.kwargs['fechaExamenId']
        fInicial = request.query_params.get('fInicial', None)
        fFinal = request.query_params.get('fFinal', None)
        if fInicial is None or fFinal is None:
            respuesta = {"detail": "Se deben indicar las fechas"}
            return Response(respuesta, status=status.HTTP_409_CONFLICT)
        
        try:
            queryset = PorExamen.objects.filter(fechaExamen=fechaExamenId, isPagado=True).values_list('id', 'medico__numRegistro', 'medico__nombre', 'medico__apPaterno', 'medico__apMaterno',
                                                                                                      'fechaExamen__fechaExamen', 'calificacion', 'medico__email', 'isAprobado', 'medico__id',
                                                                                                      'isPublicado')
            # print(f'--->>>queryset como tupla(values_list): {queryset}')
            if not queryset:
                respuesta = {"detail": "Registros no encontrados"}
                return Response(respuesta, status=status.HTTP_404_NOT_FOUND)

            for dato in queryset:
                if dato[8] and not dato[10]:  # se checa que este aprobado y no publicado
                    # hay que crear un nuevo campo de isPublicado y con ese verificar si se crea o no un certificado nuevo
                    medico = Medico.objects.get(id=dato[9])
                    Certificado.objects.create(medico=medico, documento='', descripcion='generado automaticamente por recertificacion examen', isVencido=False, estatus=1, 
                                               fechaCertificacion=fInicial, fechaCaducidad=fFinal)
                    # PorExamen.objects.filter(medico=dato[9]).update(isPublicado=True)
                    PorExamen.objects.filter(medico=dato[9]).delete()
                    
                    # se borran los registros en la tabla que es de trabajo y se mueven a la tabla para archivarlos para reportes
                    registrosAMover = list(RecertificacionItemDocumento.objects.filter(medico=dato[9]))
                    RecertificacionItemDocumento.objects.filter(medico=dato[9]).delete()
                    ArchivoDocumentosRecetificacion.objects.bulk_create(registrosAMover)
                    
                    # actualizamos a que el medico de nuevo este certificado
                    medico.isCertificado = True
                    medico.save(update_fields=['isCertificado'])

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
                print(f'--->>>datos: {datos}')
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


class CorreoDocumentosEndPoint(APIView):
    def get(self, request, *args, **kwargs):
        porExamenId = kwargs['porExamenId']
        cuentaDocumentos = PorExamenDocumento.objects.filter(porExamen=porExamenId, isAceptado=True).count()
        if cuentaDocumentos == 5:
            PorExamen.objects.filter(id=porExamenId).update(isAceptado=True)
        else:
            PorExamen.objects.filter(id=porExamenId).update(isAceptado=False)
        datosMedico = PorExamen.objects.filter(id=porExamenId).values_list('medico__nombre', 'medico__apPaterno', 'medico__apMaterno', 'medico__email')
        datos = {
            'nombre': datosMedico[0][0],
            'apPaterno': datosMedico[0][1],
            'aceptado': True if cuentaDocumentos == 5 else False,
            'email': datosMedico[0][3],
            'cuentaDocumentos': cuentaDocumentos,  # fines de control
        }
        # print(f'--->>>datos: {datos}')
        try:
            htmlContent = render_to_string('recert-doc-dig-a-r.html', datos)
            textContent = strip_tags(htmlContent)
            emailAcep = EmailMultiAlternatives('CMCPER - Documentos Aceptados/Rechazados', textContent, "no-reply@cmcper.mx", [datos['email']])
            emailAcep.attach_alternative(htmlContent, "text/html")
            emailAcep.send()
        except:
            raise ResponseError('Error al enviar correo', 500)

        return Response(datos)


class FechasExamenListView(ListAPIView):
    queryset = FechasExamenRecertificacion.objects.all()
    serializer_class = FechasExamenRecertificacionSerializer


class FechasExamenCreateView(CreateAPIView):
    serializer_class = FechasExamenRecertificacionSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = FechasExamenRecertificacionSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class FechasExamenUpdateView(UpdateAPIView):
    queryset = FechasExamenRecertificacion.objects.filter()
    serializer_class = FechasExamenRecertificacionSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']


class ProrrogaCertificadoUpdateView(UpdateAPIView):
    queryset = Certificado.objects.filter()
    serializer_class = ProrrogaCertificadoSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        dias = int(kwargs['dias'])
        id = kwargs['pk']
        try:
            dato = Certificado.objects.get(id=id)
            request.data['fechaCertificacion'] = dato.fechaCertificacion + relativedelta(days=dias)
        except:
            raise ResponseError('No existe certificado', 404)

        return self.update(request, *args, **kwargs)


class RenovacionCreateView(CreateAPIView):
    serializer_class = RenovacionSerializer

    def post(self, request, *args, **kwargs):
        serializer = RenovacionSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class RenovacionDetailView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        try:
            queryset = Renovacion.objects.filter(medico=medicoId)[0]
            serializer = RenovacionSerializer(queryset)
        except:
            raise ResponseError('No hay renovacion para el ID de Medico dado', 404)

        return Response(serializer.data)


class QRItemDocumentosCreateView(CreateAPIView):
    """
    Sólo se recibe el siguiente json:
    {
    "medico": int,
    "actividadAvalada": int
    }
    """
    serializer_class = ItemDocumentoSerializer

    def post(self, request, *args, **kwargs):
        medicoId = request.data.get('medico')
        actividadAvaladaId = request.data.get('actividadAvalada')

        request.data['estatus'] = 1
        request.data['observaciones'] = ''
        request.data['notasRechazo'] = ''
        request.data['razonRechazo'] = ''
        request.data['tituloDescripcion'] = 'Generado por QR'

        datosAA = ActividadAvalada.objects.filter(id=actividadAvaladaId)
        if datosAA.count() <= 0:
            raise ResponseError('No existe la actividad avalada', 404)
        if datosAA.get().isPagado != True:
            raise ResponseError('No esta pagada la actividad avalada', 409)

        datos = AsistenteActividadAvalada.objects.filter(medico=medicoId, actividadAvalada=actividadAvaladaId)
        if datos.count() <= 0:
            raise ResponseError('No existe el medico en la actividad avalada', 404)
        if datos.get().isPagado != True:
            raise ResponseError('No esta pagada la asistencia a la actividad avalada', 409)

        request.data['fechaEmision'] = datos.get().actividadAvalada.fechaInicio
        # request.data['puntosOtorgados'] = datos.get().actividadAvalada.puntosAsignar
        # request.data['item'] = datos.get().actividadAvalada.item.id
        if datos.get().tipo == 'Asistente':
            request.data['puntosOtorgados'] = datosAA.get().puntajeAsistente
            request.data['item'] = datosAA.get().itemAsistente.id
        if datos.get().tipo == 'Ponente':
            request.data['puntosOtorgados'] = datosAA.get().puntajePonente
            request.data['item'] = datosAA.get().itemPonente.id
        if datos.get().tipo == 'Coordinador':
            request.data['puntosOtorgados'] = datosAA.get().puntajeCoordinador
            request.data['item'] = datosAA.get().itemCoordinador.id

        serializer = ItemDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            cuenta = RecertificacionItemDocumento.objects.filter(medico=medicoId, item=request.data['item'], tituloDescripcion='Generado por QR').count()
            if cuenta > 0:
                raise ResponseError('Ya se capturo este QR', 409)
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class CodigoWEBitemDocumentosCreateView(CreateAPIView):
    """
    Sólo se recibe el siguiente json:
    {
    "medico": int,
    "codigoWeb": string
    }
    """
    serializer_class = ItemDocumentoSerializer

    def post(self, request, *args, **kwargs):
        medicoId = request.data.get('medico')
        codigoWeb = request.data.get('codigoWeb')

        request.data['estatus'] = 1
        request.data['observaciones'] = ''
        request.data['notasRechazo'] = ''
        request.data['razonRechazo'] = ''
        request.data['tituloDescripcion'] = 'Generado por QR'

        datosAA = ActividadAvalada.objects.filter(codigoWeb=codigoWeb)
        if datosAA.count() <= 0:
            raise ResponseError('No existe codigo WEB la actividad avalada', 404)
        if datosAA.get().isPagado != True:
            raise ResponseError('No esta pagada la actividad avalada', 409)

        datos = AsistenteActividadAvalada.objects.filter(medico=medicoId, actividadAvalada=datosAA.get().id)
        if datos.count() <= 0:
            raise ResponseError('No existe el medico en la actividad avalada', 404)
        if datos.get().isPagado != True:
            raise ResponseError('No esta pagada la asistencia a la actividad avalada', 409)

        request.data['fechaEmision'] = datos.get().actividadAvalada.fechaInicio
        if datos.get().tipo == 'Asistente':
            request.data['puntosOtorgados'] = datosAA.get().puntajeAsistente
            request.data['item'] = datosAA.get().itemAsistente.id
        if datos.get().tipo == 'Ponente':
            request.data['puntosOtorgados'] = datosAA.get().puntajePonente
            request.data['item'] = datosAA.get().itemPonente.id
        if datos.get().tipo == 'Coordinador':
            request.data['puntosOtorgados'] = datosAA.get().puntajeCoordinador
            request.data['item'] = datosAA.get().itemCoordinador.id

        serializer = ItemDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            cuenta = RecertificacionItemDocumento.objects.filter(medico=medicoId, item=request.data['item'], tituloDescripcion='Generado por QR').count()
            if cuenta > 0:
                raise ResponseError('Ya se capturo este QR', 409)
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class QRItemDocumentoUpdateView(UpdateAPIView):
    """
    Sólo se recibe el siguiente json:
    {
    "documento": archivoFile
    }
    """
    queryset = RecertificacionItemDocumento.objects.filter()
    serializer_class = QRItemDocumentoSerializer
    http_method_names = ['put']
