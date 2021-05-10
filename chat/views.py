from notificaciones.models import Notificacion
from rest_framework import permissions
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from api.exceptions import *
from .serializers import *
from api.logger import log
from preregistro.models import *
from rest_framework.views import APIView
from api.Paginacion import Paginacion
from rest_framework.response import Response



# Create your views here.


# ----------------------------------------------------------------------------------Chat
class ChatCreateView(CreateAPIView):
    serializer_class = MensajeSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = MensajeSerializer(data=request.data)
        if serializer.is_valid():
            destinatario = self.request.data.get('destinatario')
            # remitente = self.request.data.get('remitente')
            # print(f'--->destinatario: {destinatario}')
            Conversacion.objects.filter(destinatario=destinatario).delete()
            nombre = getNombreSesion(request,destinatario)
            Conversacion.objects.create(destinatario=destinatario,nombre=nombre)
            Notificacion.objects.create(titulo='Chat',mensaje='Tiene un nuevo mensaje',destinatario=destinatario,remitente=0)
            
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


def getNombreSesion(request,destinatario):
    nombre = request.session.get("nombre", None)
    if nombre is None:
        datosMedico = Medico.objects.filter(numRegistro=destinatario).values_list('nombre','apPaterno','apMaterno')
        nombre = str(datosMedico[0][0] + ' ' + datosMedico[0][1] + ' ' + datosMedico[0][2])
        request.session["nombre"] = nombre

    return nombre


class ChatListEndPoint(APIView):
    """
    ?size=3&page=1&orderby=id&direc=asc
    size -- es el numero de registros a traer
    page -- el numero de pagina a traer
    orderby -- campo opr el cual se ordenaran los registros a traer
    direc -- si es ascendente(asc) o descencende (vacio)
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, remitente, destinatario):
        queryset = Mensaje.objects.all().filter(remitente=remitente, destinatario=destinatario)
        size = self.request.query_params.get('size', None)
        direc = self.request.query_params.get('direc', None)
        orderby = self.request.query_params.get('orderby', None)
        page = self.request.query_params.get('page', None)

        paginacion = Paginacion(queryset, MensajeSerializer, size, direc, orderby, page)
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



class ConversacionListEndPoint(APIView):
    """
    ?size=3&page=1&orderby=id&direc=asc
    size -- es el numero de registros a traer
    page -- el numero de pagina a traer
    orderby -- campo opr el cual se ordenaran los registros a traer
    direc -- si es ascendente(asc) o descencende (vacio)
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        queryset = Conversacion.objects.all()
        size = self.request.query_params.get('size', None)
        direc = self.request.query_params.get('direc', None)
        orderby = self.request.query_params.get('orderby', None)
        page = self.request.query_params.get('page', None)

        paginacion = Paginacion(queryset, ConversacionSerializer, size, direc, orderby, page)
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
    
    
    
class MedicoChatListEndPoint(APIView):
    """
    ?size=3&page=1&orderby=id&direc=asc
    size -- es el numero de registros a traer
    page -- el numero de pagina a traer
    orderby -- campo opr el cual se ordenaran los registros a traer
    direc -- si es ascendente(asc) o descencende (vacio)
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        queryset = Medico.objects.all().filter(aceptado=True)
        size = self.request.query_params.get('size', None)
        direc = self.request.query_params.get('direc', None)
        orderby = self.request.query_params.get('orderby', None)
        page = self.request.query_params.get('page', None)

        paginacion = Paginacion(queryset, MedicoChatListSerializer, size, direc, orderby, page)
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