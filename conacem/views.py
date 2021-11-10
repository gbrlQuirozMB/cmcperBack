from api.exceptions import *
from .models import *
from .serializers import *

from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter

from api.Paginacion import Paginacion
from rest_framework.response import Response
from certificados.models import Certificado

import logging
log = logging.getLogger('django')

from rest_framework import status, permissions



class MedicosListView(ListAPIView):
    queryset = Certificado.objects.filter(isConacem=False)
    serializer_class = MedicosListSerializer
    permission_classes = (permissions.IsAdminUser,)
    
class ConacemCreateView(CreateAPIView):
    serializer_class = ConacemSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = ConacemSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors) 
