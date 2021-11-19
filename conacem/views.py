from rest_framework import status, permissions
from rest_framework.views import APIView
from api.exceptions import *
from .models import *
from .serializers import *

from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from django.http import HttpResponse
import csv
from django.views import View
from django.db.models.functions import Concat, TruncMonth, Extract


from api.Paginacion import Paginacion
from rest_framework.response import Response
from certificados.models import Certificado

import logging
log = logging.getLogger('django')


class MedicosListView(ListAPIView):
    queryset = Certificado.objects.filter(isConacem=False)
    serializer_class = MedicosListSerializer
    permission_classes = (permissions.IsAdminUser,)


class ConacemCreateView(CreateAPIView):
    serializer_class = ConacemSerializer
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        serializer = ConacemSerializer(data=request.data)
        if serializer.is_valid():
            # obtener los ids de la clave 'medicos' del json
            # medicos = request.data["medicos"]
            # ids = [x['medico'] for x in medicos]
            # con los ids cambiamos el status con el ORM de Certificados
            # NO CONVIENE PORQUE PUEDE HABER FALLOS EN LA CREACION Y YA SE CAMBIARON LOS ESTATUS
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


def renderCsvView(request, queryset):
    response = HttpResponse(content_type='text/csv')
    # response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="conacem.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['Título', 'Nombre', 'Apellido Paterno', 'Apellido Materno'])
    for dato in queryset:
        writer.writerow(dato)
        # writer.writerow(dato.encode('UTF-8'))

    return response


class ConacemDownExcel(APIView):
    def get(self, request, *args, **kwargs):
        conacemId = self.kwargs['conacemId']
        try:
            # queryset = DetalleConcacem.objects.filter(conacem=conacemId).values_list('medico__titulo', 'medico__nombre', 'medico__apPaterno', 'medico__apMaterno', 'medico__hospitalResi',
            #                                                                          'medico__hospitalResi','medico__hospLaborPrim','medico__hospLaborSec','medico__rfc')

            queryset = DetalleConcacem.objects.filter(conacem=1).annotate(
                fNd=Extract('medico__fechaNac', 'day'),
                fNm=Extract('medico__fechaNac', 'month'),
                fNa=Extract('medico__fechaNac', 'year')).values_list('medico__nombre', 'fNd', 'fNm', 'fNa')

            # print(f'--->>>queryset como tupla(values_list): {queryset}')
            if not queryset:
                respuesta = {"detail": "Registros no encontrados"}
                return Response(respuesta, status=status.HTTP_404_NOT_FOUND)

            return renderCsvView(request, queryset)
        except Exception as e:
            respuesta = {"detail": str(e)}
            return Response(respuesta, status=status.HTTP_409_CONFLICT)
