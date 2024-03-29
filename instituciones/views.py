from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from rest_framework import status, permissions

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *

# # from api.logger import log
import logging
log = logging.getLogger('django')

from api.exceptions import *

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from django.contrib.auth.models import Permission, User
from django.contrib.auth.base_user import BaseUserManager

# para crear permisos de acceso a los endpoints
# from rest_framework import exceptions


class InstitucionCreateView(CreateAPIView):
    serializer_class = InstitucionSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = InstitucionSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class InstitucionFilter(FilterSet):
    nombreInstitucionNS = CharFilter(field_name='nombreInstitucion', lookup_expr='iexact')
    contactoNS = CharFilter(field_name='contacto', lookup_expr='iexact')

    class Meta:
        model = Institucion
        fields = ['nombreInstitucionNS', 'contactoNS']


class InstitucionFilteredListView(ListAPIView):
    queryset = Institucion.objects.all()
    serializer_class = InstitucionFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = InstitucionFilter


class InstitucionDetailView(RetrieveAPIView):
    queryset = Institucion.objects.filter()
    serializer_class = InstitucionSerializer


class InstitucionUpdateView(UpdateAPIView):
    queryset = Institucion.objects.filter()
    serializer_class = InstitucionSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']


class InstitucionDeleteView(DestroyAPIView):
    queryset = Institucion.objects.filter()



# class ChatPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if not request.user.has_perm('chat.change_mensaje'):
#             raise exceptions.PermissionDenied("No tiene permisos!")
#         return True


class CorreoInstitucionEndPoint(APIView):
    # permission_classes = (ChatPermission, )

    def put(self, request, *args, **kwargs):
        institucionId = kwargs['pk']
        # datosQuery = Institucion.objects.filter(id=institucionId).values_list('id','nombreInstitucion') # solo obtener ciertos campos se usan corchetes para obtener datos
        datosQuery = Institucion.objects.filter(id=institucionId)
        if datosQuery.count() <= 0:
            raise ResponseError('No existe institucion', 404)

        nombreInstitucion = datosQuery.get().nombreInstitucion
        rfc = datosQuery.get().rfc
        email = datosQuery.get().email
        contacto = datosQuery.get().contacto

        username = nombreInstitucion[0:3] + rfc[0:3]
        password = BaseUserManager().make_random_password()  # letras mayusculas, minusculas y numeros
        username = username + '-' + password[0:5]

        user = User.objects.create_user(username=username, email=email, password=password, first_name=nombreInstitucion, last_name=contacto, is_staff=True)
        # user.user_permissions.set([153, 154, 155, 156])
        try:
            permisoView = Permission.objects.get(codename='view_actividadavaladaasistente')
            permisoDelete = Permission.objects.get(codename='delete_actividadavaladaasistente')
            permisoAdd = Permission.objects.get(codename='add_actividadavaladaasistente')
            permisoChange = Permission.objects.get(codename='change_actividadavaladaasistente')
            user.user_permissions.set([permisoView, permisoDelete, permisoAdd, permisoChange])
        except Exception as e:
            print(f'--->>>Error grave: {str(e)}')
            permisoView = Permission.objects.get(codename='view_asistenteactividadavalada')
            permisoDelete = Permission.objects.get(codename='delete_asistenteactividadavalada')
            permisoAdd = Permission.objects.get(codename='add_asistenteactividadavalada')
            permisoChange = Permission.objects.get(codename='change_asistenteactividadavalada')
            user.user_permissions.set([permisoView, permisoDelete, permisoAdd, permisoChange])
            
        Institucion.objects.filter(id=institucionId).update(username=username)

        datos = {
            # 'nombreInstitucion': datosQuery.get()[1] # si se usa 'values_list'
            'nombreInstitucion': nombreInstitucion,
            'rfc': rfc,
            'telUno': datosQuery.get().telUno,
            'email': email,
            'contacto': contacto,
            'usuario': username,
            'clave': password,
            'aceptado': True
        }
        # print(f'--->>>datos: {datos}')
        try:
            htmlContent = render_to_string('institucion.html', datos)
            textContent = strip_tags(htmlContent)
            emailAcep = EmailMultiAlternatives('CMCPER - Innstitucion datos de acceso', textContent, "no-reply@cmcper.mx", [datos['email']])
            emailAcep.attach_alternative(htmlContent, "text/html")
            emailAcep.send()
        except:
            raise ResponseError('Error al enviar correo', 500)

        return Response(datos)
        # return self.update(request, *args, **kwargs)
