from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, BooleanFilter
from rest_framework import status, permissions


from .serializers import *

from api.logger import log
from api.exceptions import *

# Create your views here.


class ActividadAvaladaCreateView(CreateAPIView):
    serializer_class = ActividadAvaladaSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = ActividadAvaladaSerializer(data=request.data)
        if serializer.is_valid():
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
    nombreNS = CharFilter(field_name='nombre', lookup_expr='iexact')
    institucionNS = CharFilter(field_name='institucion__nombreInstitucion', lookup_expr='iexact')
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


class ActividadAvaladaDeleteView(DestroyAPIView):
    queryset = ActividadAvalada.objects.filter()
    permission_classes = (permissions.IsAdminUser,)


# ------------------------ asistentes

class AsistenteActividadAvaladaCreateView(CreateAPIView):
    serializer_class = AsistenteActividadAvaladaSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        actAvaId = request.data.get('actividadAvalada')
        numAsistentes = ActividadAvalada.objects.filter(id=actAvaId).values_list('numAsistentes', flat=True)
        asistentesRegistrados = AsistenteActividadAvalada.objects.filter(actividadAvalada=actAvaId).count()
        if asistentesRegistrados >= numAsistentes[0]:
            raise ResponseError(f'No se permite registrar mas de {numAsistentes[0]} asistentes', 409)

        serializer = AsistenteActividadAvaladaSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class CuposAsistentesDetailView(RetrieveAPIView):
    queryset = ActividadAvalada.objects.filter()
    serializer_class = CuposAsistentesSerializer


class MedicosAIncribirseAAFilter(FilterSet):
    nombreNS = CharFilter(field_name='nombre', lookup_expr='iexact')
    apPaternoNS = CharFilter(field_name='apPaterno', lookup_expr='iexact')

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
    nombreNS = CharFilter(field_name='medico__nombre', lookup_expr='iexact')
    apPaternoNS = CharFilter(field_name='medico__apPaterno', lookup_expr='iexact')

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
