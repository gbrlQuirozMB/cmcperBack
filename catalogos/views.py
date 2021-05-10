from django.shortcuts import render
from rest_framework.generics import ListAPIView
from api.logger import log
from api.exceptions import *
from .serializers import *
from .models import *

from rest_framework import status, permissions
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView

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
