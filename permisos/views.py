from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from .serializers import *
from api.exceptions import *
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, DateFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.base_user import BaseUserManager


import logging
log = logging.getLogger('django')


class PermisosListView(ListAPIView):
    serializer_class = PermisosListSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        queryset = Permission.objects.all().order_by('content_type')
        return queryset


class UsuariosFilter(FilterSet):
    first_name = CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = CharFilter(field_name='last_name', lookup_expr='icontains')
    email = CharFilter(field_name='email', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UsuariosFilteredListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsuariosFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UsuariosFilter
    permission_classes = (permissions.IsAdminUser,)


class UsuariosPermisosEndPoint(APIView):
    """
    Sólo se recibe el siguiente json:
    "permisos": [
                ArrayOf: codenames: string
            ]
    """
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        try:
            usuarioId = kwargs['pk']
            permisos = request.data['permisos']

            usuario = User.objects.get(id=usuarioId)
            permisosList = []
            for dato in permisos:
                permisosList.append(Permission.objects.get(codename=dato))
            usuario.user_permissions.set(permisosList)

            datos = {
                'id': usuario.id,
                'username': usuario.username,
                'first_name': usuario.first_name,
                'last_name': usuario.last_name,
                'email': usuario.email,
                'user_permissions': usuario.get_user_permissions()
            }

            return Response(datos)
        except Exception as e:
            # log.error(f'--->>> {str(e)}')
            # respuesta = {"detail": str(e)}
            # return Response(respuesta, status=status.HTTP_409_CONFLICT)
            raise ResponseError(f'Error: {str(e)}', 409)


class UsuariosDetailView(RetrieveAPIView):
    queryset = User.objects.filter()
    serializer_class = UsuariosDetailSerializer
    permission_classes = (permissions.IsAdminUser,)


class UsuariosCreateView(CreateAPIView):
    serializer_class = UsuariosSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        request.data['password'] = BaseUserManager().make_random_password()
        serializer = UsuariosSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)
