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


