from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
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
