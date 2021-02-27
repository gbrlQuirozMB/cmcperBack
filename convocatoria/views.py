from rest_framework import response, status, permissions
from rest_framework.views import APIView
from .serializers import *
from preregistro.models import Medico
from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
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


# Create your views here.


class EsExtranjeroUpdateView(UpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = EsExtranjeroSerializer

    def put(self, request, *args, **kwargs):
        # para poder modificar el dato que llega
        request.data._mutable = True
        request.data['isExtranjero'] = True
        request.data._mutable = False

        return self.update(request, *args, **kwargs)


class EstudioExtranjeroUpdateView(UpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = EstudioExtranjeroSerializer

    def put(self, request, *args, **kwargs):
        # para poder modificar el dato que llega
        request.data._mutable = True
        request.data['estudioExtranjero'] = True
        request.data._mutable = False

        return self.update(request, *args, **kwargs)


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


class DocumentoRevalidacionCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
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
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 2
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoActaNacimientoCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 3
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCartaSolicitudCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 4
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoConstanciaPosgradoCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 5
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCedulaEspecialidadCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 6
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoTituloLicenciaturaCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 7
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCedulaProfesionalCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 8
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoConstanciaCirugiaCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 9
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class DocumentoCartaProfesorCreateView(CreateAPIView):
    serializer_class = ConvocatoriaEnroladoDocumentoSerializer

    def post(self, request, *args, **kwargs):
        request = inicializaData(request)
        request.data['catTiposDocumento'] = 10
        serializer = ConvocatoriaEnroladoDocumentoSerializer(data=request.data)
        if serializer.is_valid():
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


def render_pdf_view(request, templateSrc, datosContexto):
    template_path = templateSrc
    context = datosContexto
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
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
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
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
                'horaExamen': convocatoriaEnrolado.convocatoria.horaExamen
            }
            # print(datos)
            return render_pdf_view(request, 'pdf.html', datos)
        except:
            return HttpResponse('No se encontró el registro', content_type='text/plain')


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
        # queryset = Medico.objects.all().filter(aceptado=False)
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

    def put(self, request, *args, **kwargs):
        # para poder modificar el dato que llega
        # request.data._mutable = True
        request.data['isValidado'] = True
        # request.data._mutable = False

        return self.update(request, *args, **kwargs)


class ConvocatoriaEnroladoDocumentoRechazarUpdateView(UpdateAPIView):
    queryset = ConvocatoriaEnroladoDocumento.objects.filter()
    serializer_class = ConvocatoriaEnroladoDocumentoRechazarSerializer

    def put(self, request, *args, **kwargs):
        # para poder modificar el dato que llega
        # request.data._mutable = True
        request.data['isValidado'] = False
        # request.data._mutable = False

        return self.update(request, *args, **kwargs)

# ES DE PRUEBA NO USAR!!!
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
