from django.http import HttpResponse
import csv
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Permission, User
from rest_framework.response import Response
from api.Paginacion import Paginacion
from notificaciones.models import Notificacion
from django.shortcuts import render
from datetime import datetime

from django.conf import settings
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from api.exceptions import *
from .serializers import *
# from api.logger import log
import logging
log = logging.getLogger('django')


# ----------------------------------------------------------------------------------Preregistro


class PreregistroCreateView(CreateAPIView):
    serializer_class = MedicoSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = MedicoSerializer(data=request.data)
        if serializer.is_valid():
            datoUser = User.objects.filter(is_superuser=True, is_staff=True).values_list('id')
            Notificacion.objects.create(titulo='Preregistro', mensaje='Se creo un preregistro', destinatario=datoUser[0][0], remitente=0)
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
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
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        pk = kwargs['pk']
        # falta saber los grupos y permisos que se crearan, pero depende mas de las apps
        datosMedico = Medico.objects.filter(id=pk).values_list('nombre', 'apPaterno', 'apMaterno', 'email', 'rfc')
        username = datosMedico[0][0][0:3] + datosMedico[0][1][0:3]  # + datosMedico[0][4][4:6]
        email = datosMedico[0][3]
        lastName = datosMedico[0][1] + ' ' + datosMedico[0][2]
        # password = User.objects.make_random_password() # letras mayusculas, minusculas
        password = BaseUserManager().make_random_password()  # letras mayusculas, minusculas y numeros
        username = username + '-' + password[0:5]
        user = User.objects.create_user(username=username, email=email, password=password, first_name=datosMedico[0][0], last_name=lastName)
        permisoChMed = Permission.objects.get(codename='change_medico')
        permisoAdConv = Permission.objects.get(codename='add_conversacion')
        permisoViConv = Permission.objects.get(codename='view_conversacion')
        permisoAdMen = Permission.objects.get(codename='add_mensaje')
        permisoViMen = Permission.objects.get(codename='view_mensaje')
        # user.user_permissions.set([41, 44, 37, 40, 34])
        user.user_permissions.set([permisoChMed, permisoAdConv, permisoViConv, permisoAdMen, permisoViMen])
        # actualiza el status del registro para que este aceptado
        # Medico.objects.filter(id=pk).update(aceptado=True, numRegistro=pk, username=username)
        Medico.objects.filter(id=pk).update(aceptado=True, username=username)
        Notificacion.objects.create(titulo='Preregistro', mensaje='Su preregistro se aprobó', destinatario=pk, remitente=0)
        # print(f'--->>>password: {password}')
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
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        pk = kwargs['pk']
        Medico.objects.filter(id=pk).update(aceptado=False, numRegistro=0)
        datosMedico = Medico.objects.filter(id=pk).values_list('nombre', 'apPaterno', 'apMaterno', 'email', 'rfc')
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
            Medico.objects.filter(id=pk).delete()
        except:
            raise ResponseError('Error al enviar correo', 500)
        return self.update(request, *args, **kwargs)


class FotoPerfilUpdateView(UpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = FotoPerfilSerializer
    http_method_names = ['put']


class HorarioAtencionCreateView(CreateAPIView):
    serializer_class = HorarioAtencionSerializer

    def post(self, request, *args, **kwargs):
        serializer = HorarioAtencionSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class HorarioAtencionListView(ListAPIView):
    serializer_class = HorarioAtencionSerializer

    def get_queryset(self):
        medicoId = self.kwargs['medicoId']
        queryset = HorarioAtencion.objects.filter(medico=medicoId)
        if not queryset:
            raise ResponseError('No hay horarios de atencion', 404)
        return queryset


class HorarioAtencionDetailView(RetrieveAPIView):
    queryset = HorarioAtencion.objects.filter()
    serializer_class = HorarioAtencionSerializer


class HorarioAtencionUpdateView(UpdateAPIView):
    queryset = HorarioAtencion.objects.filter()
    serializer_class = HorarioAtencionSerializer
    http_method_names = ['put']


class HorarioAtencionDeleteView(DestroyAPIView):
    queryset = HorarioAtencion.objects.filter()


class PreregistroUpdateView(UpdateAPIView):
    queryset = Medico.objects.filter()
    serializer_class = MedicoSerializer
    http_method_names = ['put']


class NotasObservacionesCreateView(CreateAPIView):
    serializer_class = NotasObservacionesSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = NotasObservacionesSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class NotasObservacionesFilter(FilterSet):
    class Meta:
        model = NotasObservaciones
        fields = ['medico', 'tipo', 'isBorrado']


class NotasObservacionesFilteredListView(ListAPIView):
    queryset = NotasObservaciones.objects.filter()
    serializer_class = NotasObservacionesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = NotasObservacionesFilter
    permission_classes = (permissions.IsAdminUser,)


class NotasObservacionesDetailView(RetrieveAPIView):
    queryset = NotasObservaciones.objects.filter()
    serializer_class = NotasObservacionesSerializer


# def renderCsvView(request, queryset):
#     response = HttpResponse(content_type='text/csv')
#     # response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="usuarios-claves.csv"'
#     response.write(u'\ufeff'.encode('utf8'))
#     writer = csv.writer(response)
#     writer.writerow(['ID', 'Nombre', 'Apellido Paterno', 'Apellido Materno', 'Username', 'Password', 'Email'])
#     for dato in queryset:
#         writer.writerow((dato.get('id'), dato.get('nombre'), dato.get('apPaterno'), dato.get('apMaterno'), dato.get('username'), dato.get('password'), dato.get('email')))
#         # writer.writerow(dato.encode('UTF-8'))

#     return response


# class UsuariosPassEndPoint(APIView):
#     permission_classes = (permissions.AllowAny,)  # solo para probar en cliente interno thunder

#     def get(self, request, *args, **kwargs):
#         try:
#             datosMedico = Medico.objects.filter().values_list('id', 'nombre', 'apPaterno', 'apMaterno','email')
#             queryset = []
#             for dato in datosMedico:
#                 username = dato[1][0:3] + dato[2][0:3]
#                 password = BaseUserManager().make_random_password()  # letras mayusculas, minusculas y numeros
#                 username = username + '-' + password[0:5]
#                 email = dato[4]
#                 if email is None or email == '':
#                     email = (username.replace('-','.') + '@gmail.com').lower()
#                 # --- ponemos username y aceptado en medico
#                 Medico.objects.filter(id=dato[0]).update(aceptado=True, username=username, email=email)
#                 # --- creamos usuario
#                 lastName = dato[2] + ' ' + dato[3]
#                 user = User.objects.create_user(username=username, email=email, password=password, first_name=dato[1], last_name=lastName)
#                 # user = User.objects.create_user(username=username, password=password, first_name=dato[1], last_name=lastName)
#                 permisoChMed = Permission.objects.get(codename='change_medico')
#                 permisoAdConv = Permission.objects.get(codename='add_conversacion')
#                 permisoViConv = Permission.objects.get(codename='view_conversacion')
#                 permisoAdMen = Permission.objects.get(codename='add_mensaje')
#                 permisoViMen = Permission.objects.get(codename='view_mensaje')
#                 # user.user_permissions.set([41, 44, 37, 40, 34])
#                 user.user_permissions.set([permisoChMed, permisoAdConv, permisoViConv, permisoAdMen, permisoViMen])

#                 # --- para crear csv
#                 valores = {'id': dato[0], 'nombre': dato[1], 'apPaterno': dato[2], 'apMaterno': dato[3], 'username': username, 'password': password, 'email':email}
#                 queryset.append(valores)

#             if not queryset:
#                 respuesta = {"detail": "Registros no encontrados"}
#                 return Response(respuesta, status=status.HTTP_404_NOT_FOUND)

#             return renderCsvView(request, queryset)
#         except Exception as e:
#             respuesta = {"detail": str(e)}
#             return Response(respuesta, status=status.HTTP_409_CONFLICT)
