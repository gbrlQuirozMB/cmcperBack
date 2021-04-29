from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView, get_object_or_404

from .serializers import *

from notificaciones.models import Notificacion
from django.contrib.auth.models import User

from convocatoria.models import ConvocatoriaEnrolado
from recertificacion.models import PorExamen, Certificado

from api.logger import log
from api.exceptions import *

from rest_framework import response, status, permissions


# Create your views here.
class SubirPagoCreateView(CreateAPIView):
    serializer_class = PagoSerializer

    def post(self, request, *args, **kwargs):
        request.data['estatus'] = 3
        serializer = PagoSerializer(data=request.data)
        if serializer.is_valid():
            datoUser = User.objects.filter(is_superuser=True, is_staff=True).values_list('id')
            Notificacion.objects.create(titulo='Convocatoria', mensaje='Se subió un pago', destinatario=datoUser[0][0], remitente=0)
            return self.create(request, *args, **kwargs)
        log.info(f'campos incorrectos: {serializer.errors}')
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
        log.info(f'se busca por: estatus: {estatus}')

        return getQuerysetEstatus(estatus)


class PagoAceptarUpdateView(UpdateAPIView):
    queryset = Pago.objects.filter()
    serializer_class = PagoAceptarRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        id = kwargs['pk']
        try:
            dato = Pago.objects.get(id=id)
        except Exception as e:
            raise ResponseError('No existe registro', 404)

        # si se esta aceptando el pago de una CONVOCATORIA
        if dato.tipo == 1:
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
        if dato.tipo == 2:
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
        if dato.tipo == 3:
            request.data['estatus'] = 1
            medico = Medico.objects.get(id=dato.medico)
            Certificado.objects.create(medico=medico, documento='', descripcion='generado automaticamente por recertificacion renovacion', isVencido=False, estatus=1)
            return self.update(request, *args, **kwargs)


class PagoRechazarUpdateView(UpdateAPIView):
    queryset = Pago.objects.filter()
    serializer_class = PagoAceptarRechazarSerializer
    permission_classes = (permissions.IsAdminUser,)

    def put(self, request, *args, **kwargs):
        id = kwargs['pk']
        try:
            dato = Pago.objects.get(id=id)
        except Exception as e:
            raise ResponseError('No existe registro', 404)

        if dato.tipo == 1:  # si se esta aceptando el pago de una CONVOCATORIA
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

        if dato.tipo == 2:  # si se esta aceptando el pago de una RECERTIFICACION EXAMEN
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

        if dato.tipo == 3:  # si se esta aceptando el pago de una RECERTIFICACION RENOVACION
            request.data['estatus'] = 2
            return self.update(request, *args, **kwargs)
