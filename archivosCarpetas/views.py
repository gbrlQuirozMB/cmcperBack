from api.exceptions import *
from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from .serializers import *
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, DateFilter

import logging
log = logging.getLogger('django')


class CarpetaCreateView(CreateAPIView):
    serializer_class = CarpetaSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = CarpetaSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class CarpetaListView(ListAPIView):
    queryset = Carpeta.objects.all()
    serializer_class = CarpetaListSerializer


class CarpetaDetailView(RetrieveAPIView):
    queryset = Carpeta.objects.filter()
    serializer_class = CarpetaDetailSerializer


class CarpetaUpdateView(UpdateAPIView):
    queryset = Carpeta.objects.filter()
    serializer_class = CarpetaSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']


class CarpetaDeleteView(DestroyAPIView):
    queryset = Carpeta.objects.filter()


# --------------------------ARCHIVOS--------------------------

class ArchivoCreateView(CreateAPIView):
    serializer_class = ArchivoSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = ArchivoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class ArchivoFilter(FilterSet):
    class Meta:
        model = Archivo
        fields = ['carpeta']


class ArchivoFilteredListView(ListAPIView):
    queryset = Archivo.objects.all()
    serializer_class = ArchivoListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArchivoFilter


class ArchivoDetailView(RetrieveAPIView):
    queryset = Archivo.objects.filter()
    serializer_class = ArchivoDetailSerializer


class ArchivoUpdateView(UpdateAPIView):
    queryset = Archivo.objects.filter()
    serializer_class = ArchivoSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']

