from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from api.logger import log
from api.exceptions import *


# Create your views here.
# class PosicionFrontPostEndPoint(APIView):
#     def post(self, request, *args, **kwargs):
#         posicion = kwargs['posicion']
#         user = kwargs['user']
#         PosicionFront.objects.filter(user=user).delete()
#         dato = PosicionFront.objects.create(posicion=posicion, user=user)
#         respuesta = {
#             "info": "Usuario: " + user + " en posicion: " + posicion
#         }
#         return Response(respuesta, status=HTTP_201_CREATED)

class PosicionFrontCreateView(CreateAPIView):
    serializer_class = PosicionFrontSerializer

    def post(self, request, *args, **kwargs):
        request.data['posicion'] = kwargs['posicion']
        request.data['user'] = kwargs['userId']
        serializer = PosicionFrontSerializer(data=request.data)
        if serializer.is_valid():
            PosicionFront.objects.filter(user=request.data['user']).delete()
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


class PosicionFrontDetailView(RetrieveAPIView):
    queryset = PosicionFront.objects.filter()
    serializer_class = PosicionFrontLeerSerializer
    lookup_field = 'user'
    lookup_url_kwarg = 'userId'
    
