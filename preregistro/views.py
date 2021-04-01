from notificaciones.models import Notificacion
from django.shortcuts import render
from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.views import APIView

from api.exceptions import *
from .serializers import *
from api.logger import log
from api.Paginacion import Paginacion
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

# ----------------------------------------------------------------------------------Preregistro
class PreregistroCreateView(CreateAPIView):
    serializer_class = MedicoSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = MedicoSerializer(data=request.data)
        if serializer.is_valid():
            datoUser = User.objects.filter(is_superuser=True, is_staff=True).values_list('id')
            Notificacion.objects.create(titulo='Preregistro',mensaje='Se creo un preregistro',destinatario=datoUser[0][0],remitente=0)
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
    # permission_classes = (permissions.AllowAny,)

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
    # permission_classes = (permissions.AllowAny,)
    
    
class PreregistroAceptadoUpdateView(UpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = MedicoAceptadoRechazadoSerializer
    # permission_classes = (permissions.AllowAny,)
    
    def put(self, request, *args, **kwargs):
        pk = kwargs['pk']
        # falta saber los grupos y permisos que se crearan, pero depende mas de las apps
        datosMedico = Medico.objects.filter(id=pk).values_list('nombre','apPaterno','apMaterno','email','rfc')
        username = datosMedico[0][0][0:3] + datosMedico[0][1][0:3] #+ datosMedico[0][4][4:6]
        email = datosMedico[0][3]
        lastName = datosMedico[0][1] + ' ' + datosMedico[0][2]
        # password = User.objects.make_random_password() # letras mayusculas, minusculas
        password = BaseUserManager().make_random_password() # letras mayusculas, minusculas y numeros
        username = username + '-' + password[0:5]
        user = User.objects.create_user(username=username,email=email,password=password,first_name=datosMedico[0][0],last_name=lastName)
        user.user_permissions.set([41,44,37,40,34])
        # actualiza el status del registro para que este aceptado
        Medico.objects.filter(id=pk).update(aceptado=True, numRegistro=pk, username=username)
        Notificacion.objects.create(titulo='Preregistro',mensaje='Su preregistro se aprobó',destinatario=pk,remitente=0)
        try:
            datos = {
                'nombre': datosMedico[0][0],
                'apPaterno': datosMedico[0][1],
                'usuario': username,
                'clave': password,
                'aceptado': True
            }
            htmlContentAcept = render_to_string('prer-a-r.html', datos)
            textContentAcept = strip_tags(htmlContentAcept)
            emailAcep = EmailMultiAlternatives("CMCPER - Preregistro Aceptado", textContentAcept, "no-reply@cmcper.mx", [email])
            emailAcep.attach_alternative(htmlContentAcept, "text/html")
            # email.attach(filename, resultado.getvalue(), "application/pdf")
            emailAcep.send()
        except:
            raise ResponseError('Error al enviar correo', 500)
        
        return self.update(request, *args, **kwargs)
    
class PreregistroRechazadoUpdateView(UpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = MedicoAceptadoRechazadoSerializer
    # permission_classes = (permissions.AllowAny,)
    
    def put(self, request, *args, **kwargs):
        pk = kwargs['pk']
        Medico.objects.filter(id=pk).update(aceptado=False, numRegistro=0)
        datosMedico = Medico.objects.filter(id=pk).values_list('nombre','apPaterno','apMaterno','email','rfc')
        email = datosMedico[0][3]
        motivo = self.request.data.get('motivo')
        # no hay notificacion porque estas son dentro del sistema
        try:
            datos = {
                'nombre': datosMedico[0][0],
                'apPaterno': datosMedico[0][1],
                'motivo': motivo,
                'aceptado': False
            }
            htmlContentRecha = render_to_string('prer-a-r.html', datos)
            textContentRecha = strip_tags(htmlContentRecha)
            emailRecha = EmailMultiAlternatives("CMCPER - Preregistro Rechazado", textContentRecha, "no-reply@cmcper.mx", [email])
            emailRecha.attach_alternative(htmlContentRecha, "text/html")
            # email.attach(filename, resultado.getvalue(), "application/pdf")
            emailRecha.send()
            # Medico.objects.filter(id=pk).delete()
        except:
            raise ResponseError('Error al enviar correo', 500)
        return self.update(request, *args, **kwargs)
    
    
class FotoPerfilUpdateView(UpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = FotoPerfilSerializer 