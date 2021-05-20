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
