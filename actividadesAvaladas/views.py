from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, BooleanFilter, NumberFilter
from rest_framework import status, permissions

from .serializers import *

# from api.logger import log
import logging
log = logging.getLogger('django')
from api.exceptions import *

from rest_framework.views import APIView
from rest_framework.response import Response

import csv
import codecs

from django.core.exceptions import FieldError
from django.db import IntegrityError

from django.contrib.auth.base_user import BaseUserManager
from datetime import date


# from rest_framework.pagination import PageNumberPagination

# Create your views here.


class ActividadAvaladaCreateView(CreateAPIView):
    serializer_class = ActividadAvaladaSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = ActividadAvaladaSerializer(data=request.data)
        if serializer.is_valid():
            request.data['codigoWeb'] = BaseUserManager().make_random_password()  # letras mayusculas, minusculas y numeros
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class ActividadAvaladaArchivoUpdateView(UpdateAPIView):
    queryset = ActividadAvalada.objects.filter()
    serializer_class = ActividadAvaladaArchivoSerializer
    http_method_names = ['put']
    permission_classes = (permissions.IsAdminUser,)


class ActividadAvaladaBannerUpdateView(UpdateAPIView):
    queryset = ActividadAvalada.objects.filter()
    serializer_class = ActividadAvaladaBannerSerializer
    http_method_names = ['put']
    permission_classes = (permissions.IsAdminUser,)



# PAGINACION
# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 2
#     page_size_query_param = 'page_size'
#     max_page_size = 3



class ActividadAvaladaFilter(FilterSet):
    nombreNS = CharFilter(field_name='nombre', lookup_expr='icontains')
    institucionNS = CharFilter(field_name='institucion__nombreInstitucion', lookup_expr='icontains')
    pagado = CharFilter(field_name='isPagado')
    idInstitucion = NumberFilter(field_name='institucion_id', lookup_expr='exact')

    class Meta:
        model = ActividadAvalada
        fields = ['nombreNS', 'institucionNS', 'pagado', 'idInstitucion']


class ActividadAvaladaFilteredListView(ListAPIView):
    queryset = ActividadAvalada.objects.all()
    serializer_class = ActividadAvaladaFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ActividadAvaladaFilter
    permission_classes = (permissions.IsAdminUser,)
    # pagination_class = StandardResultsSetPagination


class ActividadAvaladaDetailView(RetrieveAPIView):
    queryset = ActividadAvalada.objects.filter()
    serializer_class = ActividadAvaladaDetailSerializer


class ActividadAvaladaUpdateView(UpdateAPIView):
    queryset = ActividadAvalada.objects.filter()
    serializer_class = ActividadAvaladaSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        id = kwargs['pk']
        try:
            datos = ActividadAvalada.objects.get(id=id)
            if datos.isPagado == True:
                raise ResponseError(f'No se puede cambiar, la actividad ya esta pagada', 409)
            cuenta = AsistenteActividadAvalada.objects.filter(actividadAvalada=id).count()
            if cuenta > 0:
                request.data['institucion'] = datos.institucion.id
        except ActividadAvalada.DoesNotExist:
            raise ResponseError(f'No encontrado.', 404)

        return self.update(request, *args, **kwargs)


class ActividadAvaladaDeleteView(DestroyAPIView):
    queryset = ActividadAvalada.objects.filter()
    permission_classes = (permissions.IsAdminUser,)


class ActividadAvaladaPorPagarDetailView(RetrieveAPIView):
    queryset = ActividadAvalada.objects.filter()
    serializer_class = ActividadAvaladaPorPagarSerializer


# ------------------------ asistentes

class AsistenteActividadAvaladaCreateView(CreateAPIView):
    serializer_class = AsistenteActividadAvaladaSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        actAvaId = request.data.get('actividadAvalada')
        medicoId = request.data.get('medico')
        cuenta = AsistenteActividadAvalada.objects.filter(medico=medicoId, actividadAvalada=actAvaId).count()
        if cuenta > 0:
            raise ResponseError(f'Ya esta registrado el medico', 409)

        serializer = AsistenteActividadAvaladaSerializer(data=request.data)
        if serializer.is_valid():
            ActividadAvalada.objects.filter(id=actAvaId).update(isPagado=False)
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class MedicosAIncribirseAAFilter(FilterSet):
    nombreNS = CharFilter(field_name='nombre', lookup_expr='icontains')
    apPaternoNS = CharFilter(field_name='apPaterno', lookup_expr='icontains')

    class Meta:
        model = Medico
        fields = ['nombreNS', 'apPaternoNS']


class MedicosAIncribirseAAFilteredListView(ListAPIView):
    queryset = Medico.objects.filter(aceptado=True)
    serializer_class = MedicosAIncribirseAASerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedicosAIncribirseAAFilter
    permission_classes = (permissions.IsAdminUser,)


class MedicosAsistenteAAFilter(FilterSet):
    nombreNS = CharFilter(field_name='medico__nombre', lookup_expr='icontains')
    apPaternoNS = CharFilter(field_name='medico__apPaterno', lookup_expr='icontains')

    class Meta:
        model = AsistenteActividadAvalada
        fields = ['nombreNS', 'apPaternoNS', 'actividadAvalada']


class MedicosAsistenteAAFilteredListView(ListAPIView):
    queryset = AsistenteActividadAvalada.objects.all()
    serializer_class = MedicosAsistenteAASerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MedicosAsistenteAAFilter
    permission_classes = (permissions.IsAdminUser,)


class MedicosAsistenteAADeleteView(DestroyAPIView):
    queryset = AsistenteActividadAvalada.objects.filter()
    permission_classes = (permissions.IsAdminUser,)


class ActividadAvaladaPagadoView(UpdateAPIView):
    queryset = ActividadAvalada.objects.filter()
    serializer_class = ActividadAvaladaPagadoSerializer
    # permission_classes = (permissions.IsAdminUser,) # No porque se utiliza desde un usuario normal
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        request.data['isPagado'] = True
        actAvaId = kwargs['pk']
        AsistenteActividadAvalada.objects.filter(actividadAvalada=actAvaId).update(isPagado=True)
        return self.update(request, *args, **kwargs)


class AsistentesUpExcel(APIView):
    def post(self, request, *args, **kwargs):
        actAvaId = kwargs['pk']
        datoAA = ActividadAvalada.objects.get(id=actAvaId)

        if datoAA.fechaLimite <= date.today():
            log.error(f'--->>> Fecha limite alcanzada, no puede cargar asistentes')
            raise ResponseError('Fecha limite alcanzada, no puede cargar asistentes', 409)

        AsistenteActividadAvalada.objects.filter(actividadAvalada=actAvaId).delete()

        archivo = request.data['archivo']
        # archivo = request.FILES['archivo']
        datosList = list(csv.reader(codecs.iterdecode(archivo, 'utf-8', errors='ignore'), delimiter=','))
        # datosList = list(csv.reader(codecs.iterdecode(archivo, 'utf-8'), delimiter=','))
        datosList.pop(0)
        try:
            # datos = {'dadosAlta':[]}
            # valorReng = {'numCertificado': 0,'nombre':''}
            for row in datosList:
                datoMedico = Medico.objects.get(numRegistro=row[0])
                AsistenteActividadAvalada.objects.create(medico=datoMedico, actividadAvalada=datoAA, tipo=row[4].title())
                # valorReng = {'numCertificado': row[0],'nombre': row[1]}
                # datos['dadosAlta'].append(valorReng)

            AsistenteActividadAvalada.objects.exclude(tipo__in=['Asistente', 'Ponente', 'Coordinador']).delete()  # borrar registros que no cumplan con nombre correctos
            cuenta = AsistenteActividadAvalada.objects.filter(actividadAvalada=actAvaId).count()
            respuesta = {"detail": "Se borraron los registros anteriores e incorrectos. Datos subidos correctamente"}
            respuesta['numRegistrosSubidos'] = cuenta
            # respuesta['detail'] = datos
            ActividadAvalada.objects.filter(id=actAvaId).update(isPagado=False)
            return Response(respuesta, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            log.error(f'--->>> Sólo puede existir un Medico asistente por Actividad Avalada')
            respuesta = {"detail": "Sólo puede existir un Medico asistente por Actividad Avalada"}
            return Response(respuesta, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            log.error(f'--->>> {str(e)}')
            respuesta = {"detail": str(e)}
            return Response(respuesta, status=status.HTTP_409_CONFLICT)
