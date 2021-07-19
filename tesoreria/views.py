from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView, get_object_or_404

from .serializers import *

from notificaciones.models import Notificacion
from django.contrib.auth.models import User

from convocatoria.models import ConvocatoriaEnrolado
from recertificacion.models import PorExamen, Renovacion, RecertificacionItemDocumento
from certificados.models import Certificado
from actividadesAvaladas.models import ActividadAvalada, AsistenteActividadAvalada
from catalogos.models import CatPagos

# from api.logger import log
import logging
log = logging.getLogger('django')
from api.exceptions import *

from rest_framework import response, status, permissions

from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, BooleanFilter



# Create your views here.
class SubirPagoCreateView(CreateAPIView):
    serializer_class = PagoSerializer

    def post(self, request, *args, **kwargs):
        request.data['estatus'] = 3
        serializer = PagoSerializer(data=request.data)
        if serializer.is_valid():
            datoUser = User.objects.filter(is_superuser=True, is_staff=True).values_list('id') # obteniendo al admin
            datosCatalogo = CatPagos.objects.get(id=request.data.get('tipo')) # obteniendo la descripcion del tipo de pago
            Notificacion.objects.create(titulo=datosCatalogo.descripcion, mensaje='Se subió un pago', destinatario=datoUser[0][0], remitente=0)
            return self.create(request, *args, **kwargs)
        log.error(f'--->>>campos incorrectos: {serializer.errors}')
        raise CamposIncorrectos(serializer.errors)


def getQuerysetEstatus(estatus):
    if estatus == 0:
        queryset = Pago.objects.all()
        return queryset

    queryset = Pago.objects.filter(estatus=estatus)
    return queryset


class PagosListView(ListAPIView):
    serializer_class = PagosListSerializer

    def get_queryset(self):
        estatus = self.kwargs['estatus']
        log.error(f'--->>>se busca por: estatus: {estatus}')

        return getQuerysetEstatus(estatus)


class PagoAceptarUpdateView(UpdateAPIView):
    queryset = Pago.objects.filter()
    serializer_class = PagoAceptarRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        id = kwargs['pk']
        try:
            dato = Pago.objects.get(id=id)
        except Exception as e:
            raise ResponseError('No existe registro', 404)

        # si se esta aceptando el pago de una CONVOCATORIA
        if dato.tipo == 2 or dato.tipo == 3 or dato.tipo == 4:
            verificador = ConvocatoriaEnrolado.objects.filter(id=dato.externoId)
            if not verificador:
                raise ResponseError('No existe el ID de convocatoria', 404)
            cuenta = ConvocatoriaEnrolado.objects.filter(id=dato.externoId, isAceptado=True).count()
            if cuenta == 1:
                request.data['estatus'] = 1
                ConvocatoriaEnrolado.objects.filter(id=dato.externoId).update(isPagado=True)
                return self.update(request, *args, **kwargs)
            cuenta = ConvocatoriaEnrolado.objects.filter(id=dato.externoId).count()
            if cuenta == 1:
                raise ResponseError('No tiene permitido pagar', 409)

        # si se esta aceptando el pago de una RECERTIFICACION EXAMEN
        if dato.tipo == 1:
            verificador = PorExamen.objects.filter(id=dato.externoId)
            if not verificador:
                raise ResponseError('No existe el ID de porExamen', 404)
            cuenta = PorExamen.objects.filter(id=dato.externoId, isAceptado=True).count()
            if cuenta == 1:
                request.data['estatus'] = 1
                PorExamen.objects.filter(id=dato.externoId).update(isPagado=True)
                return self.update(request, *args, **kwargs)
            cuenta = PorExamen.objects.filter(id=dato.externoId).count()
            if cuenta == 1:
                raise ResponseError('No tiene permitido pagar', 409)

        # si se esta aceptando el pago de una RECERTIFICACION RENOVACION
        if dato.tipo == 6:
            verificador = Renovacion.objects.filter(id=dato.externoId)
            if not verificador:
                raise ResponseError('No existe el ID de renovacion', 404)
            cuenta = Renovacion.objects.filter(id=dato.externoId).count()
            if cuenta == 1:
                request.data['estatus'] = 1
                Renovacion.objects.filter(id=dato.externoId).delete()
                RecertificacionItemDocumento.objects.filter(medico=dato.medico.id).delete()
                # Medico.objects.filter(id=dato.medico.id).update(isCertificado=True)  #quiza no sea tan buena idea meter aqui el update porque es un proceso de tesoreria
                return self.update(request, *args, **kwargs)
        
        # si se esta aceptando el pago de una ACTIVIDAD AVALADA
        if dato.tipo == 5:
            verificador = ActividadAvalada.objects.filter(id=dato.externoId)
            if not verificador:
                raise ResponseError('No existe el ID de actividad avalada', 404)
            cuenta = ActividadAvalada.objects.filter(id=dato.externoId).count()
            if cuenta == 1:
                request.data['estatus'] = 1
                ActividadAvalada.objects.filter(id=dato.externoId).update(isPagado=True) # ponemos en pagado a la Act Avala
                AsistenteActividadAvalada.objects.filter(actividadAvalada=dato.externoId).update(isPagado=True) # ponemos en pagado a los asistentes de la Act Avala
                return self.update(request, *args, **kwargs)

class PagoRechazarUpdateView(UpdateAPIView):
    queryset = Pago.objects.filter()
    serializer_class = PagoAceptarRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)
    http_method_names = ['put']

    def put(self, request, *args, **kwargs):
        id = kwargs['pk']
        try:
            dato = Pago.objects.get(id=id)
        except Exception as e:
            raise ResponseError('No existe registro', 404)

        if dato.tipo == 2 or dato.tipo == 3 or dato.tipo == 4:  # si se esta rechazando el pago de una CONVOCATORIA
            verificador = ConvocatoriaEnrolado.objects.filter(id=dato.externoId)
            if not verificador:
                raise ResponseError('No existe el ID de convocatoria', 404)
            cuenta = ConvocatoriaEnrolado.objects.filter(id=dato.externoId, isAceptado=True).count()
            if cuenta == 1:
                request.data['estatus'] = 2
                ConvocatoriaEnrolado.objects.filter(id=dato.externoId).update(isPagado=False)
                return self.update(request, *args, **kwargs)
            cuenta = ConvocatoriaEnrolado.objects.filter(id=dato.externoId).count()
            if cuenta == 1:
                raise ResponseError('No tiene permitido pagar', 409)

        if dato.tipo == 1:  # si se esta rechazando el pago de una RECERTIFICACION EXAMEN
            verificador = PorExamen.objects.filter(id=dato.externoId)
            if not verificador:
                raise ResponseError('No existe el ID de porExamen', 404)
            cuenta = PorExamen.objects.filter(id=dato.externoId, isAceptado=True).count()
            if cuenta == 1:
                request.data['estatus'] = 2
                PorExamen.objects.filter(id=dato.externoId).update(isPagado=False)
                return self.update(request, *args, **kwargs)
            cuenta = PorExamen.objects.filter(id=dato.externoId).count()
            if cuenta == 1:
                raise ResponseError('No tiene permitido pagar', 409)

        if dato.tipo == 6:  # si se esta rechazando el pago de una RECERTIFICACION RENOVACION
            verificador = Renovacion.objects.filter(id=dato.externoId)
            if not verificador:
                raise ResponseError('No existe el ID de renovacion', 404)
            cuenta = Renovacion.objects.filter(id=dato.externoId).count()
            if cuenta == 1:
                request.data['estatus'] = 2
                Renovacion.objects.filter(id=dato.externoId).update(isPagado=False)
                return self.update(request, *args, **kwargs)
            # return self.update(request, *args, **kwargs)
            raise ResponseError('No tiene permitido pagar', 409)
        
        # si se esta aceptando el pago de una ACTIVIDAD AVALADA
        if dato.tipo == 5:
            verificador = ActividadAvalada.objects.filter(id=dato.externoId)
            if not verificador:
                raise ResponseError('No existe el ID de actividad avalada', 404)
            cuenta = ActividadAvalada.objects.filter(id=dato.externoId).count()
            if cuenta == 1:
                request.data['estatus'] = 2
                ActividadAvalada.objects.filter(id=dato.externoId).update(isPagado=False) # ponemos en pagado a la Act Avala
                AsistenteActividadAvalada.objects.filter(actividadAvalada=dato.externoId).update(isPagado=False) # ponemos en pagado a los asistentes de la Act Avala
                return self.update(request, *args, **kwargs)


class PagoFilter(FilterSet):
    class Meta:
        model = Pago
        fields = ['medico', 'tipo', 'externoId']


class PagoFilteredListView(ListAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagosListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PagoFilter