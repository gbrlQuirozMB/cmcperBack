from api.exceptions import *
from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from .serializers import *
from rest_framework import permissions

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
