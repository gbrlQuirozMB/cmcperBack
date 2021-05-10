from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView

from .serializers import *

from api.logger import log
from api.exceptions import *


# Create your views here.
class ComunicadoCreateView(CreateAPIView):
    serializer_class = ComunicadoSerializer

    def post(self, request, *args, **kwargs):
        serializer = ComunicadoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)
