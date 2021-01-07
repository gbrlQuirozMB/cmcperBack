from django.shortcuts import render
from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView

from api.exceptions import *
from .serializers import *
from api.logger import log

# Create your views here.


# ----------------------------------------------------------------------------------Preregistro
class PreregistroCreateView(CreateAPIView):
    serializer_class = MedicoSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = MedicoSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)
