from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework import status, permissions
from .models import *
from .serializers import *
from api.exceptions import *
from django.shortcuts import render
from rest_framework.generics import ListAPIView
# from api.logger import log
import logging
log = logging.getLogger('django')


# Create your views here.


class CatMotivoRechazoListView(ListAPIView):
    serializer_class = CatMotivosRechazoFilteredSerializer

    def get_queryset(self):
        textoBusqueda = self.kwargs['textoBusqueda']
        # log.error(f'--->>>se busca por: textoBusqueda: {textoBusqueda}')
        if textoBusqueda == 'all':
            queryset = CatMotivosRechazo.objects.filter()
            return queryset

        queryset = CatMotivosRechazo.objects.filter(descripcion__icontains=textoBusqueda)
        return queryset


class CatMotivosRechazoCreateView(CreateAPIView):
    serializer_class = CatMotivosRechazoSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = CatMotivosRechazoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class CatMotivosRechazoUpdateView(UpdateAPIView):
    queryset = CatMotivosRechazo.objects.filter()
    serializer_class = CatMotivosRechazoSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']


class CatMotivosRechazoDeleteView(DestroyAPIView):
    queryset = CatMotivosRechazo.objects.filter()


class CatPagosCreateView(CreateAPIView):
    serializer_class = CatPagosSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = CatPagosSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class CatPagosFilter(FilterSet):
    descripcionNS = CharFilter(field_name='descripcion', lookup_expr='icontains')

    class Meta:
        model = CatPagos
        # fields = ['descripcionNS', 'tipo']
        fields = ['descripcionNS']


class CatPagosFilteredListView(ListAPIView):
    queryset = CatPagos.objects.all()
    serializer_class = CatPagosFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CatPagosFilter
    permission_classes = (permissions.IsAdminUser,)


class CatPagosUpdateView(UpdateAPIView):
    queryset = CatPagos.objects.filter()
    serializer_class = CatPagosSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']


class CatEntidadListView(ListAPIView):
    queryset = CatEntidad.objects.all()
    serializer_class = CatEntidadListSerializer
    permission_classes = (permissions.AllowAny,)


class CatSedesListView(ListAPIView):
    queryset = CatSedes.objects.all()
    serializer_class = CatSedesSerializer
    permission_classes = (permissions.AllowAny,)
