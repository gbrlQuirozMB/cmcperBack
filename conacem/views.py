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
    response = HttpResponse(content_type='text/csv', charset='utf-8')
    # response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="conacem.csv"'
    # response.write(u'\ufeff'.encode('UTF-8'))
    writer = csv.writer(response)
    writer.writerow(['Título', 'Nombre', 'Apellido Paterno', 'Apellido Materno', 'Universidad de egreso de la especialidad', 'Institución de residencia de la especialidad',
                     'Institución dónde labora', 'Hospital privado dónde labora', 'R.F.C.', 'CURP', 'Cédula profesional de médico general', 'FN-Día', 'FN-Mes', 'FN-Año', 'Nacionalidad',
                     'Estado donde radica', 'Municipio', 'Género Femenino = F Masculino = M', 'FEC-Día', 'FEC-Mes', 'FEC-Año', 'VDe-Día', 'VDe-Mes', 'VDe-Año', 'VAl-Día', 'VAl-Mes', 'VAl-Año',
                     'No. Certificado', 'Libro', 'Foja', 'Título', 'Presidente', 'Título', 'Responsable', 'Costo', 'Email', 'Observaciones', 'Cédula de la especialidad'])
    # writer.writerow([u'Hóla'.encode('utf-8')])
    # writer.writerow([u'Hóla'.encode('iso-8859-1')])
    for dato in queryset:
        writer.writerow(dato)
        # writer.writerow([unicode(v).encode('utf-8') if v is not None else '' for v in row])
    
    
    
    
        
    return response


class ConacemDownExcel(APIView):
    # permission_classes = (permissions.AllowAny,)
    permission_classes = (permissions.IsAdminUser,)
    
    def get(self, request, *args, **kwargs):
        conacemId = self.kwargs['conacemId']
        try:
            queryset = DetalleConcacem.objects.filter(
                conacem=1, medico__medicoC__isConacem=False).annotate(
                fNd=Extract('medico__fechaNac', 'day'),
                fNm=Extract('medico__fechaNac', 'month'),
                fNa=Extract('medico__fechaNac', 'year'),
                fEd=Extract('conacem__fechaEmision', 'day'),
                fEm=Extract('conacem__fechaEmision', 'month'),
                fEa=Extract('conacem__fechaEmision', 'year'),
                fVDd=Extract('conacem__fechaValidezDel', 'day'),
                fVDm=Extract('conacem__fechaValidezDel', 'month'),
                fVDa=Extract('conacem__fechaValidezDel', 'year'),
                fVAd=Extract('conacem__fechaValidezAl', 'day'),
                fVAm=Extract('conacem__fechaValidezAl', 'month'),
                fVAa=Extract('conacem__fechaValidezAl', 'year')).values_list(
                'medico__titulo', 'medico__nombre', 'medico__apPaterno', 'medico__apMaterno', 'medico__hospitalResi', 'medico__hospitalResi', 'medico__hospLaborPrim', 'medico__hospLaborSec',
                'medico__rfc', 'medico__curp', 'medico__cedProfesional', 'fNd', 'fNm', 'fNa', 'medico__nacionalidad', 'medico__estado', 'medico__deleMuni', 'medico__sexo', 'fEd', 'fEm', 'fEa',
                'fVDd', 'fVDm', 'fVDa', 'fVAd', 'fVAm', 'fVAa', 'medico__medicoC__id', 'libro', 'foja', 'conacem__tituloPresidente', 'conacem__nombrePresidente', 'conacem__tituloResponsable',
                'conacem__nombreResponsable', 'conacem__costo', 'medico__email', 'observaciones', 'medico__cedEspecialidad')

            # print(f'--->>>queryset como tupla(values_list): {queryset}')
            if not queryset:
                respuesta = {"detail": "Registros no encontrados"}
                return Response(respuesta, status=status.HTTP_404_NOT_FOUND)

            return renderCsvView(request, queryset)
        except Exception as e:
            respuesta = {"detail": str(e)}
            return Response(respuesta, status=status.HTTP_409_CONFLICT)
