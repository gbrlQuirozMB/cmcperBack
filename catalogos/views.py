from django.shortcuts import render
from rest_framework.generics import ListAPIView
from api.logger import log
from api.exceptions import *
from .serializers import *
from .models import *

from rest_framework import status, permissions
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter


# Create your views here.


class MotivoRechazoListView(ListAPIView):
    serializer_class = CatMotivosRechazoSerializer

    def get_queryset(self):
        textoBusqueda = self.kwargs['textoBusqueda']
        log.info(f'se busca por: textoBusqueda: {textoBusqueda}')
        queryset = CatMotivosRechazo.objects.filter(descripcion__icontains=textoBusqueda)

        return queryset


class CatPagosCreateView(CreateAPIView):
    serializer_class = CatPagosSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = CatPagosSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class CatPagosFilter(FilterSet):
    descripcionNS = CharFilter(field_name='descripcion', lookup_expr='iexact')

    class Meta:
        model = CatPagos
        fields = ['descripcionNS', 'tipo']


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
