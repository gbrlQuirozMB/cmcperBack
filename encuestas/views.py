from api.exceptions import *
from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from .serializers import *
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, DateFilter


import logging
log = logging.getLogger('django')


class EncuestaCreateView(CreateAPIView):
    serializer_class = EncuestaSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = EncuestaSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class EncuestaFilter(FilterSet):
    fechaInicioNS = DateFilter(field_name='fechaInicio', lookup_expr="lte")
    fechaFinNS = DateFilter(field_name='fechaFin', lookup_expr="gte")

    class Meta:
        model = Encuesta
        fields = ['estatus', 'regionGeografica', 'isSoloConsejero', 'fechaInicioNS', 'fechaFinNS']


class EncuestaFilteredListView(ListAPIView):
    queryset = Encuesta.objects.all()
    serializer_class = EncuestaListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EncuestaFilter


class EncuestaDetailView(RetrieveAPIView):
    queryset = Encuesta.objects.filter()
    serializer_class = EncuestaDetailSerializer


class EncuestaUpdateView(UpdateAPIView):
    queryset = Encuesta.objects.filter()
    serializer_class = EncuestaSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']


class EncuestaDeleteView(DestroyAPIView):
    queryset = Encuesta.objects.filter()


# --------------------------PREGUNTAS--------------------------

class PreguntaCreateView(CreateAPIView):
    serializer_class = PreguntaSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        id = kwargs['pk']
        request.data['encuesta'] = id
        serializer = PreguntaSerializer(data=request.data)
        if serializer.is_valid():
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class PreguntaListView(ListAPIView):
    serializer_class = PreguntaListSerializer

    def get_queryset(self):
        encuesta = self.kwargs['pk']
        queryset = Pregunta.objects.filter(encuesta=encuesta)
        return queryset


class PreguntaDetailView(RetrieveAPIView):
    queryset = Pregunta.objects.filter()
    serializer_class = PreguntaDetailSerializer


class PreguntaUpdateView(UpdateAPIView):
    queryset = Pregunta.objects.filter()
    serializer_class = PreguntaSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']
