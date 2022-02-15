from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from .serializers import *
from api.exceptions import *
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, DateFilter


class PermisosListView(ListAPIView):
    serializer_class = PermisosListSerializer

    def get_queryset(self):
        queryset = Permission.objects.all().order_by('content_type')
        return queryset


class UsuariosFilter(FilterSet):
    nombreNS = CharFilter(field_name='first_name', lookup_expr='icontains')
    apellidosNS = CharFilter(field_name='last_name', lookup_expr='icontains')
    emailNS = CharFilter(field_name='email', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username', 'nombreNS', 'apellidosNS', 'emailNS']


class UsuariosFilteredListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsuariosFilteredListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UsuariosFilter
