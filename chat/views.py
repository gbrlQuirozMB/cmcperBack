from rest_framework import permissions
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from api.exceptions import *
from .serializers import *
from api.logger import log
from preregistro.models import *
# Create your views here.


# ----------------------------------------------------------------------------------Chat
class ChatCreateView(CreateAPIView):
    serializer_class = MensajeSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = MensajeSerializer(data=request.data)
        if serializer.is_valid():
            destinatario = self.request.data.get('destinatario')
            remitente = self.request.data.get('remitente')
            Conversacion.objects.filter(destinatario=destinatario).delete()
            nombre = getNombreSesion(request,destinatario)
            Conversacion.objects.create(destinatario=destinatario,nombre=nombre)
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