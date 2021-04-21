from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from preregistro.models import Medico

from api.logger import log
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
    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        try:
            queryset = Certificado.objects.filter(medico=medicoId)[0]
            serializer = CertificadoDatosSerializer(queryset)
        except:
            raise ResponseError('No hay certificado para el ID de Medico dado', 404)

        return Response(serializer.data)


class AvanceMedicoCapituloDetailView(RetrieveAPIView):
    # serializer_class = AvanceMedicoCapituloSerializer

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
        queryset = RecertificacionItemDocumento.objects.filter(item=itemId)
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
        log.info(f'campos incorrectos: {serializer.errors}')
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
        log.info(f'se busca por:  estatus: {estatus} - nombre: {nombre} - apPaterno: {apPaterno}')

        return getQuerysetItemDocumentosFiltered(estatus, nombre, apPaterno)


class ItemDocumentosDetailView(RetrieveAPIView):
    queryset = RecertificacionItemDocumento.objects.filter()
    serializer_class = ItemDocumentoDetailSerializer


class ItemDocumentosAceptar(UpdateAPIView):
    queryset = RecertificacionItemDocumento.objects.filter()
    serializer_class = ItemDocumentoAceptarRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        request.data['estatus'] = 1
        request.data['notasRechazo'] = ''
        request.data['razonRechazo'] = ''

        return self.update(request, *args, **kwargs)


class ItemDocumentosRechazar(UpdateAPIView):
    queryset = RecertificacionItemDocumento.objects.filter()
    serializer_class = ItemDocumentoAceptarRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        request.data['estatus'] = 2
        request.data['puntosOtorgados'] = 0

        return self.update(request, *args, **kwargs)


class ItemDocumentosReasignar(UpdateAPIView):
    queryset = RecertificacionItemDocumento.objects.filter()
    serializer_class = ItemDocumentoReasignarSerializer
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        request.data['estatus'] = 1
        request.data['notasRechazo'] = ''
        request.data['razonRechazo'] = ''

        return self.update(request, *args, **kwargs)


class CapituloListView(ListAPIView):
    queryset = Capitulo.objects.all()
    serializer_class = CapituloListSerializer


class SubcapituloListView(ListAPIView):
    serializer_class = SubcapituloListSerializer

    def get_queryset(self):
        capituloId = self.kwargs['capituloId']
        queryset = Subcapitulo.objects.filter(capitulo=capituloId)
        if not queryset:
            raise ResponseError('No existen subcapitulos con el capituloId proporcionado', 404)
        return queryset


class ItemListView(ListAPIView):
    serializer_class = ItemListSerializer

    def get_queryset(self):
        subcapituloId = self.kwargs['subcapituloId']
        queryset = Item.objects.filter(subcapitulo=subcapituloId)
        if not queryset:
            raise ResponseError('No existen items con el subcapituloId proporcionado', 404)
        return queryset


class ActualizaVigenciaCertificados(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        try:
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
                raise ResponseError('El medico tiene una solicitud de examen pendiente', 409)
            datosMedico = Medico.objects.filter(id=medicoId).values_list('nombre', 'apPaterno', 'apMaterno', 'email')
            queryset = FechasExamenRecertificacion.objects.filter(fechaExamen__gte=date.today())
            queryset = queryset.order_by('fechaExamen')[:1]
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
        log.info(f'campos incorrectos: {serializer.errors}')
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
    if cuentaDocumentos == 1:  # porque ya borro antes el que ya existia
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
        log.info(f'campos incorrectos: {serializer.errors}')
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
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class PorExamenAPagarEndPoint(APIView):
    def getQuerySet(self):
        try:
            return CatPagos.objects.get(tipo=1)
        except CatPagos.DoesNotExist:
            raise ResponseError('No existe un registro de pago para el Examen Certificación Vigente', 404)

    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        cuenta = Medico.objects.filter(id=medicoId).count()
        if cuenta < 1:
            raise ResponseError('No existe medico',404)
        queryset = self.getQuerySet()
        serializer = MedicoAPagarSerializer(queryset, context={'medicoId': medicoId})
        return Response(serializer.data)


class RenovacionAPagarEndPoint(APIView):
    def getQuerySet(self):
        try:
            return CatPagos.objects.get(tipo=6)
        except CatPagos.DoesNotExist:
            raise ResponseError('No existe un registro de pago para Renovación de Certificación', 404)

    def get(self, request, *args, **kwargs):
        medicoId = kwargs['medicoId']
        cuenta = Medico.objects.filter(id=medicoId).count()
        if cuenta < 1:
            raise ResponseError('No existe medico',404)
        queryset = self.getQuerySet()
        serializer = MedicoAPagarSerializer(queryset, context={'medicoId': medicoId})
        return Response(serializer.data)