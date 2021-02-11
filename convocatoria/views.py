from rest_framework import response
from .serializers import *
from preregistro.models import Medico
from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView


# Create your views here.
class EsExtranjeroUpdateView(UpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = EsExtranjeroSerializer
    
    def put(self, request, *args, **kwargs):
        # para poder modificar el dato que llega
        request.data._mutable = True
        request.data['isExtranjero'] = True
        request.data._mutable = False
        
        return self.update(request, *args, **kwargs)


class EstudioExtranjeroUpdateView(UpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = EstudioExtranjeroSerializer

    def put(self, request, *args, **kwargs):
        # para poder modificar el dato que llega
        request.data._mutable = True
        request.data['estudioExtranjero'] = True
        request.data._mutable = False
        
        return self.update(request, *args, **kwargs)
