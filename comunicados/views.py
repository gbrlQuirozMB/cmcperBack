from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from rest_framework import status, permissions


from .serializers import *

# from api.logger import log
import logging
log = logging.getLogger('django')
from api.exceptions import *


# Create your views here.
class ComunicadoCreateView(CreateAPIView):
    serializer_class = ComunicadoSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = ComunicadoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class ComunicadoFilter(FilterSet):
    tituloNS = CharFilter(field_name='titulo', lookup_expr='iexact')

    class Meta:
        model = Comunicado
        fields = ['tituloNS', 'categoria']


class ComunicadoFilteredListView(ListAPIView):
    queryset = Comunicado.objects.all()
    serializer_class = ComunicadoFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ComunicadoFilter


class ComunicadoDetailView(RetrieveAPIView):
    queryset = Comunicado.objects.filter()
    serializer_class = ComunicadoFilteredListSerializer


class ComunicadoUpdateView(UpdateAPIView):
    queryset = Comunicado.objects.filter()
    serializer_class = ComunicadoSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']


class ComunicadoDeleteView(DestroyAPIView):
    queryset = Comunicado.objects.filter()
