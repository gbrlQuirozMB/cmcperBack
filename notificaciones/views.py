from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from notificaciones.serializers import NotificacionLeerSerializer, NotificacionSerializer
from notificaciones.models import Notificacion
from django.shortcuts import render
from rest_framework.views import APIView
from api.Paginacion import Paginacion
from rest_framework.response import Response
from rest_framework import permissions

# Create your views here.

class NotificacionListEndPoint(APIView):
    """
    ?size=3&page=1&orderby=id&direc=asc
    size -- es el numero de registros a traer
    page -- el numero de pagina a traer
    orderby -- campo opr el cual se ordenaran los registros a traer
    direc -- si es ascendente(asc) o descencende (vacio)
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, destinatario):
        queryset = Notificacion.objects.all().filter(destinatario=destinatario, leido=False)
        size = self.request.query_params.get('size', None)
        direc = self.request.query_params.get('direc', None)
        orderby = self.request.query_params.get('orderby', None)
        page = self.request.query_params.get('page', None)

        paginacion = Paginacion(queryset, NotificacionSerializer, size, direc, orderby, page)
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
    
    
class NotificacionLeerUpdateView(RetrieveUpdateAPIView):
    queryset = Notificacion.objects.filter()
    serializer_class = NotificacionLeerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def put(self, request, *args, **kwargs):
        pk = kwargs['pk']
        Notificacion.objects.filter(id=pk).update(leido=True)

        return self.update(request, *args, **kwargs)
