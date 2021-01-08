from django.shortcuts import render
from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView

from api.exceptions import *
from .serializers import *
from api.logger import log
from api.Paginacion import Paginacion
from rest_framework.response import Response


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


class PreregistroListEndPoint(APIView):
    """
    ?size=3&page=1&orderby=id&direc=asc
    size -- es el numero de registros a traer
    page -- el numero de pagina a traer
    orderby -- campo opr el cual se ordenaran los registros a traer
    direc -- si es ascendente(asc) o descencende (vacio)
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        queryset = Medico.objects.all().filter(aceptado=False)
        size = self.request.query_params.get('size', None)
        direc = self.request.query_params.get('direc', None)
        orderby = self.request.query_params.get('orderby', None)
        page = self.request.query_params.get('page', None)

        paginacion = Paginacion(queryset, MedicoListSerializer, size, direc, orderby, page)
        serializer = paginacion.paginar()

        respuesta = {
            "totalElements": paginacion.totalElements,
            "totalPages": paginacion.totalPages,
            "sort": paginacion.orderby,
            "direction": paginacion.direc,
            "size": paginacion.size,
            "content": serializer.data
        }
        return Response(respuesta)


class PreregistroDetailView(RetrieveAPIView):
    queryset = Medico.objects.filter()
    serializer_class = MedicoSerializer
    permission_classes = (permissions.AllowAny,)
    
    
class PreregistroUpdateView(RetrieveUpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = MedicoAceptadoSerializer
    permission_classes = (permissions.AllowAny,)
    
    def put(self, request, *args, **kwargs):
        pk = kwargs['pk']
        Medico.objects.filter(id=pk).update(aceptado=True, numRegistro=pk)
        
        return self.update(request, *args, **kwargs)