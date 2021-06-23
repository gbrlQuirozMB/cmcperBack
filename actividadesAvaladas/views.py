from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, BooleanFilter
from rest_framework import status, permissions

from .serializers import *

from api.logger import log
from api.exceptions import *

from rest_framework.views import APIView
from rest_framework.response import Response

import csv
import codecs

from django.core.exceptions import FieldError
from django.db import IntegrityError

from django.contrib.auth.base_user import BaseUserManager


# Create your views here.


class ActividadAvaladaCreateView(CreateAPIView):
    serializer_class = ActividadAvaladaSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = ActividadAvaladaSerializer(data=request.data)
        if serializer.is_valid():
            request.data['codigoWeb'] = BaseUserManager().make_random_password()  # letras mayusculas, minusculas y numeros
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
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


class ActividadAvaladaFilter(FilterSet):
    nombreNS = CharFilter(field_name='nombre', lookup_expr='icontains')
    institucionNS = CharFilter(field_name='institucion__nombreInstitucion', lookup_expr='icontains')
    pagado = CharFilter(field_name='isPagado')

    class Meta:
        model = ActividadAvalada
        fields = ['nombreNS', 'institucionNS', 'pagado']


class ActividadAvaladaFilteredListView(ListAPIView):
    queryset = ActividadAvalada.objects.all()
    serializer_class = ActividadAvaladaFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ActividadAvaladaFilter
    permission_classes = (permissions.IsAdminUser,)


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

        # ya no existen numAsistentes, porque los asistentes se va creando cobre la marcha
        # numAsistentes = ActividadAvalada.objects.filter(id=actAvaId).values_list('numAsistentes', flat=True)
        # if not numAsistentes:
        #     raise ResponseError(f'No existe Actividad avalada', 404)

        # ya no existen numAsistentes, porque los asistentes se va creando cobre la marcha
        # asistentesRegistrados = AsistenteActividadAvalada.objects.filter(actividadAvalada=actAvaId).count()
        # if asistentesRegistrados >= numAsistentes[0]:
        #     raise ResponseError(f'No se permite registrar mas de {numAsistentes[0]} asistentes', 409)

        medicoId = request.data.get('medico')
        cuenta = AsistenteActividadAvalada.objects.filter(medico=medicoId, actividadAvalada=actAvaId).count()
        if cuenta > 0:
            raise ResponseError(f'Ya esta registrado el medico', 409)

        serializer = AsistenteActividadAvaladaSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)

# ya no existen cupos, porque los asistentes se va creando cobre la marcha
# class CuposAsistentesDetailView(RetrieveAPIView):
#     queryset = ActividadAvalada.objects.filter()
#     serializer_class = CuposAsistentesSerializer


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
        return self.update(request, *args, **kwargs)


class AsistentesUpExcel(APIView):
    def post(self, request, *args, **kwargs):
        actAvaId = kwargs['pk']
        datoAA = ActividadAvalada.objects.get(id=actAvaId)
        AsistenteActividadAvalada.objects.filter(actividadAvalada=actAvaId).delete()

        archivo = request.data['archivo']
        datosList = list(csv.reader(codecs.iterdecode(archivo, 'utf-8'), delimiter=','))
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
            return Response(respuesta, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            respuesta = {"detail": "Sólo puede existir un Medico asistente por Actividad Avalada"}
            return Response(respuesta, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            respuesta = {"detail": str(e)}
            return Response(respuesta, status=status.HTTP_409_CONFLICT)
