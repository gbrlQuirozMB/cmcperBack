from .serializers import *
from preregistro.models import Medico
from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView


# Create your views here.
class esExtranjeroUpdateView(UpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = ExtranjeroSerializer