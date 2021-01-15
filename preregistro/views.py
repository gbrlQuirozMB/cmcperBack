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

from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager


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
    
    
class PreregistroAceptadoUpdateView(RetrieveUpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = MedicoAceptadoRechazadoSerializer
    permission_classes = (permissions.AllowAny,)
    
    def put(self, request, *args, **kwargs):
        pk = kwargs['pk']
        Medico.objects.filter(id=pk).update(aceptado=True, numRegistro=pk)
        # falta saber los grupos y permisos que se crearan, pero depende mas de las apps
        datosMedico = Medico.objects.filter(id=1).values_list('nombre','apPaterno','apMaterno','email','rfc')
        username = datosMedico[0][0][0:3] + datosMedico[0][1][0:3] + datosMedico[0][4][4:6]
        # password = User.objects.make_random_password() # letras mayusculas, minusculas
        password = BaseUserManager().make_random_password() # letras mayusculas, minusculas y numeros
        user = User.objects.create_user(username=username,email=datosMedico[0][3],password=password,first_name=datosMedico[0][0],last_name=datosMedico[0][1])
        user.user_permissions.set([41,44,37,40,34])
        # falta enviar por correo el nuevo usuarios creado pero eso lo HACE el FRONT desde otro endpoint
        return self.update(request, *args, **kwargs)
    
class PreregistroRechazadoUpdateView(RetrieveUpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = MedicoAceptadoRechazadoSerializer
    permission_classes = (permissions.AllowAny,)
    
    def put(self, request, *args, **kwargs):
        pk = kwargs['pk']
        Medico.objects.filter(id=pk).update(aceptado=False, numRegistro=0)
        # falta enviar por correo el motivo del rechazo pero eso lo HACE el FRONT desde otro endpoint
        return self.update(request, *args, **kwargs)