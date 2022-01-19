from api.exceptions import *
from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from .serializers import *
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter


import logging
log = logging.getLogger('django')


class EntregaFisicaCreateView(CreateAPIView):
    serializer_class = EntregaFisicaSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = EntregaFisicaSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class EntregaFisicaFilter(FilterSet):
    nombreRecibeNS = CharFilter(field_name='nombreRecibe', lookup_expr='icontains')

    class Meta:
        model = EntregaFisica
        fields = ['nombreRecibeNS', 'fechaEntrega', 'medico']


class EntregaFisicaFilteredListView(ListAPIView):
    queryset = EntregaFisica.objects.all()
    serializer_class = EntregaFisicaFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EntregaFisicaFilter


class EntregaFisicaDetailView(RetrieveAPIView):
    queryset = EntregaFisica.objects.filter()
    serializer_class = EntregaFisicaDetailSerializer


class EntregaFisicaUpdateView(UpdateAPIView):
    queryset = EntregaFisica.objects.filter()
    serializer_class = EntregaFisicaSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']


class EntregaFisicaDeleteView(DestroyAPIView):
    queryset = EntregaFisica.objects.filter()


class CatTiposDocumentoEntregaCreateView(CreateAPIView):
    serializer_class = CatTiposDocumentoEntregaSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = CatTiposDocumentoEntregaSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class CatTiposDocumentoEntregaListView(ListAPIView):
    queryset = CatTiposDocumentoEntrega.objects.all()
    serializer_class = CatTiposDocumentoEntregaListSerializer
