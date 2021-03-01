from django.shortcuts import render
from rest_framework.generics import ListAPIView
from api.logger import log
from api.exceptions import *
from .serializers import *
from .models import *

# Create your views here.
class MotivoRechazoListView(ListAPIView):
    serializer_class = CatMotivosRechazoSerializer

    def get_queryset(self):
        textoBusqueda = self.kwargs['textoBusqueda']
        print(f'--->>>textoBusqueda: {textoBusqueda}')
        log.info(f'se busca por: textoBusqueda: {textoBusqueda}')
        queryset = CatMotivosRechazo.objects.filter(descripcion__icontains=textoBusqueda)

        return queryset