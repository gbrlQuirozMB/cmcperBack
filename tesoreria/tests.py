from django.test import TestCase

from convocatoria.models import Convocatoria, ConvocatoriaEnrolado
from preregistro.models import Medico
from catalogos.models import *
from recertificacion.models import PorExamen, FechasExamenRecertificacion

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from io import BytesIO, StringIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from .serializers import *
import json

from datetime import date
from dateutil.relativedelta import relativedelta

import requests

from notificaciones.models import Notificacion
from certificados.models import Certificado
from recertificacion.models import Capitulo, Subcapitulo, Item
from instituciones.models import Institucion
from actividadesAvaladas.models import ActividadAvalada


# Create your tests here.
class PostSubirPago200Test(APITestCase):
    def setUp(self):
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(id=1, descripcion='tiposExameneDescripcion1', precio=111.11, precioExtrangero=222.22)
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(id=3, descripcion='tiposExameneDescripcion3', precio=333.33, precioExtrangero=444.44)

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles6')

        ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico6, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3, isAceptado=True)

        archivo = open('./uploads/testUnit.png', 'rb')
        comprobante = SimpleUploadedFile(archivo.name, archivo.read(), content_type='image/png')

        self.json = {
            "medico": 9,
            "concepto": "concepto del pago",
            "comprobante": comprobante,
            "monto": 369.99,
            "nota": "nota del pago",
            "tipo": 1,  # viene desde el front que obtuvo de los endpoints de /a-pagar/
            "externoId": 3
            # "estatus": 3
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/tesoreria/subir-pago/create/', data=self.json, format='multipart')
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cuenta = Notificacion.objects.count()
        if cuenta != 0:
            dato = Notificacion.objects.get(id=1)
            print(f'--->>>dato: titulo: {dato.titulo}, mensaje: {dato.mensaje}, destinatario: {dato.destinatario}, remitente: {dato.remitente}')


class GetPagoList200Test(APITestCase):
    def setUp(self):
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)
        
        CatPagos.objects.create(descripcion='Examen Certificación Vigente', precio=123.45)
        CatPagos.objects.create(descripcion='Examen Convocatoria Nacional', precio=456.78)
        CatPagos.objects.create(descripcion='Examen Convocatoria Extranjero', precio=369.69)
        CatPagos.objects.create(descripcion='Examen Especial de Certificación', precio=333.33)
        CatPagos.objects.create(descripcion='Actividad Asistencial', precio=666.66)
        CatPagos.objects.create(descripcion='Renovación de Certificación', precio=999.99)

        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(id=1, descripcion='tiposExameneDescripcion1', precio=111.11, precioExtrangero=222.22)
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(id=3, descripcion='tiposExameneDescripcion3', precio=333.33, precioExtrangero=444.44)

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles6')

        convocatoriaEnrolado1 = ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria1, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        convocatoriaEnrolado2 = ConvocatoriaEnrolado.objects.create(medico=medico6, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        convocatoriaEnrolado3 = ConvocatoriaEnrolado.objects.create(medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3, isAceptado=True)

        Pago.objects.create(medico=medico3, concepto='concepto', comprobante='archvivo', monto=333.33, nota='nota', estatus=3, tipo=1, externoId=1)
        Pago.objects.create(medico=medico6, concepto='concepto', comprobante='archvivo', monto=666.66, nota='nota', estatus=2, tipo=1, externoId=2)
        Pago.objects.create(medico=medico9, concepto='concepto', comprobante='archvivo', monto=999.99, nota='nota', estatus=1, tipo=2, externoId=3)
        Pago.objects.create(medico=medico9, concepto='concepto', comprobante='archvivo', monto=999.99, nota='nota', estatus=1, tipo=99, externoId=3)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/tesoreria/pagos/0/list/')  # regresa TODOS
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/tesoreria/pagos/3/list/')  # regresa pendientes
        # print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutPagoAceptar200Test(APITestCase):
    def setUp(self):
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(id=1, descripcion='tiposExameneDescripcion1', precio=111.11, precioExtrangero=222.22)
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(id=3, descripcion='tiposExameneDescripcion3', precio=333.33, precioExtrangero=444.44)

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles6')

        ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1, isAceptado=False)
        ConvocatoriaEnrolado.objects.create(medico=medico6, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3, isAceptado=True)

        fechaExamen1 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-04-01', descripcion='primer fecha')
        PorExamen.objects.create(id=6, medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=True, fechaExamen=fechaExamen1)
        
        institucion3 = Institucion.objects.create(nombreInstitucion='nombre institucion 3', rfc='rfc 3', contacto='contacto 3', telUno='telUno 3', telDos='telDos 3', telCelular='telCelular 3',
                                                  email='email 3', pais='pais 3', estado='estado 3', ciudad='ciudad 3', deleMuni='deleMuni 3', colonia='colonia 3', calle='calle 3', cp='cp 3',
                                                  numInterior='Interior 3', numExterior='Exterior 3')
        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)
        
        ActividadAvalada.objects.create(institucion=institucion3, item=item1, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 6', solicitante='solicitante 6', tipoPago=2, porcentaje=33, precio=0, descripcion='descripcion 6', isPagado=False)

        Pago.objects.create(id=3, medico=medico3, concepto='concepto', comprobante='archvivo', monto=333.33, nota='nota', estatus=3, tipo=1, externoId=1)
        Pago.objects.create(id=6, medico=medico6, concepto='concepto', comprobante='archvivo', monto=666.66, nota='nota', estatus=3, tipo=1, externoId=6)  # recertificaion por examen -> 1
        Pago.objects.create(id=9, medico=medico9, concepto='concepto', comprobante='archvivo', monto=999.99, nota='nota', estatus=3, tipo=3, externoId=3)  # convocatoria enrolado -> 2 3 4
        Pago.objects.create(id=12, medico=medico9, concepto='concepto', comprobante='archvivo', monto=999.99, nota='nota', estatus=3, tipo=5, externoId=1)  # actividad avalada -> 5
        

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated - IsAdminUser

    def test(self):
        self.client.force_authenticate(user=self.user)

        # ---------------------------------------------------------------------
        print('\n PAGO A ACTIVIDAD AVALADA')
        dato = Pago.objects.get(id=12)
        print(f'--->>>ANTES Pago: {dato.id} - {dato.estatus}')
        dato = ActividadAvalada.objects.get(id=1)
        print(f'--->>>ANTES ActividadAvalada: {dato.id} - {dato.isPagado}')

        response = self.client.put('/api/tesoreria/pago/aceptar/12/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Pago.objects.get(id=12)
        print(f'--->>>DESPUES Pago: {dato.id} - {dato.estatus}')
        dato = ActividadAvalada.objects.get(id=1)
        print(f'--->>>DESPUES ActividadAvalada: {dato.id} - {dato.isPagado}')

        print('\n PAGO A CONVOCATORIA NO EXISTE EL REGISTRO EN TABLA convocatoria')
        Pago.objects.filter(id=12).update(externoId=4)
        response = self.client.put('/api/tesoreria/pago/aceptar/12/')
        print(f'response JSON ===>>> 404 no encontrado \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


        # ---------------------------------------------------------------------
        # print('\n PAGO A CONVOCATORIA')
        # dato = Pago.objects.get(id=9)
        # print(f'--->>>ANTES Pago: {dato.id} - {dato.estatus}')
        # dato = ConvocatoriaEnrolado.objects.get(id=3)
        # print(f'--->>>ANTES ConvocatoriaEnrolado: {dato.id} - {dato.isPagado}')

        # response = self.client.put('/api/tesoreria/pago/aceptar/9/')
        # print(f'response JSON ===>>> OK \n {json.dumps(response.data)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # dato = Pago.objects.get(id=9)
        # print(f'--->>>DESPUES Pago: {dato.id} - {dato.estatus}')
        # dato = ConvocatoriaEnrolado.objects.get(id=3)
        # print(f'--->>>DESPUES ConvocatoriaEnrolado: {dato.id} - {dato.isPagado}')

        # print('\n PAGO A CONVOCATORIA NO EXISTE EL REGISTRO EN TABLA convocatoria')
        # Pago.objects.filter(id=9).update(externoId=4)
        # response = self.client.put('/api/tesoreria/pago/aceptar/9/')
        # print(f'response JSON ===>>> 404 no encontrado \n {json.dumps(response.data)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------

        # print('\n PAGO A POR EXAMEN')
        # dato = Pago.objects.get(id=6)
        # print(f'--->>>ANTES Pago: {dato.id} - {dato.estatus}')
        # dato = PorExamen.objects.get(id=6)
        # print(f'--->>>ANTES PorExamen: {dato.id} - {dato.isPagado}')

        # response = self.client.put('/api/tesoreria/pago/aceptar/6/')
        # print(f'response JSON ===>>> OK \n {json.dumps(response.data)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # dato = Pago.objects.get(id=6)
        # print(f'--->>>DESPUES Pago: {dato.id} - {dato.estatus}')
        # dato = PorExamen.objects.get(id=6)
        # print(f'--->>>DESPUES PorExamen: {dato.id} - {dato.isPagado}')

        # print('\n PAGO A POR EXAMEN NO EXISTE EL REGISTRO EN TABLA porExamen')
        # Pago.objects.filter(id=6).update(externoId=1)
        # response = self.client.put('/api/tesoreria/pago/aceptar/6/')
        # print(f'response JSON ===>>> 404 no encontrado \n {json.dumps(response.data)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # ---------------------------------------------------------------------

        # print('\n')
        # ConvocatoriaEnrolado.objects.filter(id=3).update(isAceptado=False)
        # response = self.client.put('/api/tesoreria/pago/aceptar/9/')
        # print(f'response JSON ===>>> 409 no tiene permitido pagar \n {json.dumps(response.data)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # print('\n')
        # response = self.client.put('/api/tesoreria/pago/aceptar/99/')
        # print(f'response JSON ===>>> 404 no encontrado \n {json.dumps(response.data)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PutPagoRechazar200Test(APITestCase):
    def setUp(self):
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(id=1, descripcion='tiposExameneDescripcion1', precio=111.11, precioExtrangero=222.22)
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(id=3, descripcion='tiposExameneDescripcion3', precio=333.33, precioExtrangero=444.44)

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles6')

        ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1, isAceptado=False)
        ConvocatoriaEnrolado.objects.create(medico=medico6, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3, isAceptado=True)

        fechaExamen1 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-04-01', descripcion='primer fecha')
        PorExamen.objects.create(id=6, medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=True, fechaExamen=fechaExamen1)

        Pago.objects.create(id=3, medico=medico3, concepto='concepto', comprobante='archvivo', monto=333.33, nota='nota', estatus=3, tipo=1, externoId=1)
        Pago.objects.create(id=6, medico=medico6, concepto='concepto', comprobante='archvivo', monto=666.66, nota='nota', estatus=3, tipo=2, externoId=6)  # recertificaion por examen
        Pago.objects.create(id=9, medico=medico9, concepto='concepto', comprobante='archvivo', monto=999.99, nota='nota', estatus=3, tipo=1, externoId=3)  # convocatoria enrolado

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated - IsAdminUser

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = Pago.objects.get(id=9)
        print(f'--->>>ANTES Pago: {dato.id} - {dato.estatus}')
        dato = ConvocatoriaEnrolado.objects.get(id=3)
        print(f'--->>>ANTES ConvocatoriaEnrolado: {dato.id} - {dato.isPagado}')

        response = self.client.put('/api/tesoreria/pago/rechazar/9/')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Pago.objects.get(id=9)
        print(f'--->>>DESPUES Pago: {dato.id} - {dato.estatus}')
        dato = ConvocatoriaEnrolado.objects.get(id=3)
        print(f'--->>>DESPUES ConvocatoriaEnrolado: {dato.id} - {dato.isPagado}')

        ConvocatoriaEnrolado.objects.filter(id=3).update(isAceptado=False)
        response = self.client.put('/api/tesoreria/pago/rechazar/9/')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        response = self.client.put('/api/tesoreria/pago/rechazar/99/')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
