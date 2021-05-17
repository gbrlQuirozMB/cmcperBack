from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from rest_framework import status, permissions


from .serializers import *

from api.logger import log
from api.exceptions import *
# Create your views here.


class InstitucionCreateView(CreateAPIView):
    serializer_class = InstitucionSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = InstitucionSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
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
