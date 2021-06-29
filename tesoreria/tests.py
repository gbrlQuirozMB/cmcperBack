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
from actividadesAvaladas.models import ActividadAvalada, AsistenteActividadAvalada
from catalogos.models import CatPagos



def configDB():
    CatPagos.objects.create(descripcion='Examen Certificación Vigente', precio=111.11)
    CatPagos.objects.create(descripcion='Examen Convocatoria Nacional', precio=222.22)
    CatPagos.objects.create(descripcion='Examen Convocatoria Extranjero', precio=333.33)
    CatPagos.objects.create(descripcion='Examen Especial de Certificación', precio=444.44)
    CatPagos.objects.create(descripcion='Actividad Asistencial', precio=555.55)
    CatPagos.objects.create(descripcion='Renovación de Certificación', precio=666.66)
    
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
    
    institucion1 = Institucion.objects.create(nombreInstitucion='nombre institucion 1', rfc='rfc 1', contacto='contacto 1', telUno='telUno 1', telDos='telDos 1', telCelular='telCelular 1',
                                              email='email 1', pais='pais 1', estado='estado 1', ciudad='ciudad 1', deleMuni='deleMuni 1', colonia='colonia 1', calle='calle 1', cp='cp 1',
                                              numInterior='Interior 1', numExterior='Exterior 1')
    institucion2 = Institucion.objects.create(nombreInstitucion='nombre institucion 2', rfc='rfc 2', contacto='contacto 2', telUno='telUno 2', telDos='telDos 2', telCelular='telCelular 2',
                                              email='email 2', pais='pais 2', estado='estado 2', ciudad='ciudad 2', deleMuni='deleMuni 2', colonia='colonia 2', calle='calle 2', cp='cp 2',
                                              numInterior='Interior 2', numExterior='Exterior 2')
    institucion3 = Institucion.objects.create(nombreInstitucion='nombre institucion 3', rfc='rfc 3', contacto='contacto 3', telUno='telUno 3', telDos='telDos 3', telCelular='telCelular 3',
                                              email='email 3', pais='pais 3', estado='estado 3', ciudad='ciudad 3', deleMuni='deleMuni 3', colonia='colonia 3', calle='calle 3', cp='cp 3',
                                              numInterior='Interior 3', numExterior='Exterior 3')

    convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
    convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles6')

    convocatoriaEnrolado1 = ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria1, catSedes=catSedes1, catTiposExamen=catTiposExamen1, isAceptado=False)
    convocatoriaEnrolado2 = ConvocatoriaEnrolado.objects.create(medico=medico6, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
    convocatoriaEnrolado3 = ConvocatoriaEnrolado.objects.create(medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3, isAceptado=True)
    
    
    fechaExamen1 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-04-01', descripcion='primer fecha')
    PorExamen.objects.create(id=6, medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=True, fechaExamen=fechaExamen1)
    
    # capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
    # subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
    # item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)
    
    aa1 = ActividadAvalada.objects.create(institucion=institucion3, nombre='nombre 3', emailContacto='emailContacto 3',
                                    fechaInicio=date.today() + relativedelta(days=8), fechaLimite=date.today() + relativedelta(days=16),
                                    lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=33, precio=369.69, descripcion='descripcion 3', isPagado=False, codigoWeb='E27tpSgr2c')
    aa2 = ActividadAvalada.objects.create(institucion=institucion3, nombre='nombre 3', emailContacto='emailContacto 3',
                                    fechaInicio=date.today() + relativedelta(days=8), fechaLimite=date.today() + relativedelta(days=16),
                                    lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=33, precio=369.69, descripcion='descripcion 3', isPagado=False, codigoWeb='E27tpSgr2c')
    
    AsistenteActividadAvalada.objects.create(medico=medico6, actividadAvalada=aa1, tipo='Asistente')
    AsistenteActividadAvalada.objects.create(medico=medico6, actividadAvalada=aa2, tipo='Asistente')
    AsistenteActividadAvalada.objects.create(medico=medico9, actividadAvalada=aa2, tipo='Asistente')
    
    Pago.objects.create(id=3, medico=medico3, concepto='concepto 3', comprobante='archvivo_3.jpg', monto=333.33, nota='nota 3', estatus=1, tipo=2, externoId=1)
    Pago.objects.create(id=6, medico=medico6, concepto='concepto 6', comprobante='archvivo_6.jpg', monto=666.66, nota='nota 6', estatus=3, tipo=1, externoId=6)  # recertificaion por examen -> 1
    Pago.objects.create(id=9, medico=medico9, concepto='concepto 9', comprobante='archvivo_9.jpg', monto=999.99, nota='nota 9', estatus=3, tipo=3, externoId=3)  # convocatoria enrolado -> 2 3 4
    Pago.objects.create(id=12, institucion=institucion2, concepto='concepto 12', comprobante='archvivo_12.jpg', monto=1212.12, nota='nota 12', estatus=3, tipo=5, externoId=2, numeroPago=3)  # actividad avalada -> 5
    


class PostSubirPago200Test(APITestCase):
    def setUp(self):
        
        configDB()
        
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

        archivo = open('./uploads/testUnit.png', 'rb')
        comprobante = SimpleUploadedFile(archivo.name, archivo.read(), content_type='image/png')

        self.json = {
            "medico": 9,
            "concepto": "concepto del pago",
            "comprobante": comprobante,
            "monto": 369.99,
            "nota": "nota del pago",
            "tipo": 1,  # viene desde el front que obtuvo de los endpoints de /a-pagar/  cat_pagos->Examen Certificación Vigente
            "externoId": 3 # viene desde el front que obtuvo de los endpoints de /a-pagar/ id del registro que va a pagar
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # response = self.client.post('/api/tesoreria/subir-pago/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> ok pago de ExCerVig \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # self.json['tipo'] = 2
        # response = self.client.post('/api/tesoreria/subir-pago/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> ok pago de Convocatoria \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.json['tipo'] = 5
        self.json['institucion'] = 3
        self.json['numeroPago'] = 6
        self.json.pop('medico',None)
        # del self.json['medico'] 
        response = self.client.post('/api/tesoreria/subir-pago/create/', data=self.json, format='multipart')
        print(f'response JSON ===>>> ok pago de ActAsist \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
        
        cuenta = Notificacion.objects.count()
        if cuenta != 0:
            dato = Notificacion.objects.get(id=1)
            print(f'--->>>dato: titulo: {dato.titulo}, mensaje: {dato.mensaje}, destinatario: {dato.destinatario}, remitente: {dato.remitente}')
        


class GetPagoList200Test(APITestCase):
    def setUp(self):
        
        configDB()
        
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)
        
        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/tesoreria/pagos/0/list/')  # regresa TODOS
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/tesoreria/pagos/1/list/')  # regresa aceptados
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutPagoAceptar200Test(APITestCase):
    def setUp(self):
        
        configDB() 
        
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated - IsAdminUser

    def test(self):
        self.client.force_authenticate(user=self.user)

        # ---------------------------------------------------------------------
        # print('\n PAGO A ACTIVIDAD AVALADA')
        # # dato = Pago.objects.get(id=12)
        # # print(f'--->>>ANTES Pago: {dato.id} - {dato.estatus}')
        # # dato = ActividadAvalada.objects.get(id=2)
        # # print(f'--->>>ANTES ActividadAvalada: {dato.id} - {dato.isPagado}')
        # # datosAAA = AsistenteActividadAvalada.objects.filter()
        # # for dato in datosAAA:
        # #     print(f'--->>>ANTES AsistenteActividadAvalada: {dato.id} - {dato.isPagado} - {dato.actividadAvalada.id}')
            
        # self.assertEqual(Pago.objects.get(id=12).estatus, 3) # valor inicial estatus == 3 (pendiente)
        # self.assertEqual(ActividadAvalada.objects.get(id=2).isPagado, False) # valor iincial isPagado == False
        # self.assertEqual(AsistenteActividadAvalada.objects.filter(actividadAvalada=2, isPagado=False).count(),2) # existen 3 asistentes, 2 pertenecen a ActAval 2, valor inicial False
        

        # response = self.client.put('/api/tesoreria/pago/aceptar/12/')
        # print(f'response JSON ===>>> OK \n {json.dumps(response.data)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # # dato = Pago.objects.get(id=12)
        # # print(f'--->>>DESPUES Pago: {dato.id} - {dato.estatus}')
        # # dato = ActividadAvalada.objects.get(id=2)
        # # print(f'--->>>DESPUES ActividadAvalada: {dato.id} - {dato.isPagado}')
        # # datosAAA = AsistenteActividadAvalada.objects.filter()
        # # for dato in datosAAA:
        # #     print(f'--->>>DESPUES AsistenteActividadAvalada: {dato.id} - {dato.isPagado} - {dato.actividadAvalada.id}')
        
        # self.assertEqual(Pago.objects.get(id=12).estatus, 1)
        # self.assertEqual(ActividadAvalada.objects.get(id=2).isPagado, True)
        # self.assertEqual(AsistenteActividadAvalada.objects.filter(actividadAvalada=2, isPagado=True).count(),2)  

        # print('\n PAGO A CONVOCATORIA NO EXISTE EL REGISTRO EN TABLA convocatoria')
        # Pago.objects.filter(id=12).update(externoId=666) # se pone un ID inexistente de una actividad avalada
        # response = self.client.put('/api/tesoreria/pago/aceptar/12/')
        # print(f'response JSON ===>>> 404 no encontrado \n {json.dumps(response.data)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


        # ---------------------------------------------------------------------
        print('\n PAGO A CONVOCATORIA')
        # dato = Pago.objects.get(id=9)
        # print(f'--->>>ANTES Pago: {dato.id} - {dato.estatus}')
        # dato = ConvocatoriaEnrolado.objects.get(id=3)
        # print(f'--->>>ANTES ConvocatoriaEnrolado: {dato.id} - {dato.isPagado}\n')
        
        self.assertEqual(Pago.objects.get(id=9).estatus, 3)
        self.assertEqual(ConvocatoriaEnrolado.objects.get(id=3).isPagado, False)

        response = self.client.put('/api/tesoreria/pago/aceptar/9/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # dato = Pago.objects.get(id=9)
        # print(f'--->>>DESPUES Pago: {dato.id} - {dato.estatus}')
        # dato = ConvocatoriaEnrolado.objects.get(id=3)
        # print(f'--->>>DESPUES ConvocatoriaEnrolado: {dato.id} - {dato.isPagado}\n')
        
        self.assertEqual(Pago.objects.get(id=9).estatus, 1)
        self.assertEqual(ConvocatoriaEnrolado.objects.get(id=3).isPagado, True)
        
        ConvocatoriaEnrolado.objects.filter(id=3).update(isAceptado=False)
        response = self.client.put('/api/tesoreria/pago/aceptar/9/')
        print(f'response JSON ===>>> 409 no permitido pagar \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        print('\n PAGO A CONVOCATORIA NO EXISTE EL REGISTRO EN TABLA convocatoria')
        Pago.objects.filter(id=9).update(externoId=666)
        response = self.client.put('/api/tesoreria/pago/aceptar/9/')
        print(f'response JSON ===>>> 404 no encontrado \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


        # ---------------------------------------------------------------------
        # print('\n PAGO A POR EXAMEN')
        # # dato = Pago.objects.get(id=6)
        # # print(f'--->>>ANTES Pago: {dato.id} - {dato.estatus}')
        # # dato = PorExamen.objects.get(id=6)
        # # print(f'--->>>ANTES PorExamen: {dato.id} - {dato.isPagado}')
        # self.assertEqual(Pago.objects.get(id=6).estatus, 3)
        # self.assertEqual(PorExamen.objects.get(id=6).isPagado, False)

        # response = self.client.put('/api/tesoreria/pago/aceptar/6/')
        # print(f'response JSON ===>>> OK \n {json.dumps(response.data)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # # dato = Pago.objects.get(id=6)
        # # print(f'--->>>DESPUES Pago: {dato.id} - {dato.estatus}')
        # # dato = PorExamen.objects.get(id=6)
        # # print(f'--->>>DESPUES PorExamen: {dato.id} - {dato.isPagado}\n')
        # self.assertEqual(Pago.objects.get(id=6).estatus, 1)
        # self.assertEqual(PorExamen.objects.get(id=6).isPagado, True)
        
        # Pago.objects.filter(id=6).update(estatus=3)
        # PorExamen.objects.filter(id=6).update(isAceptado=False, isPagado=False)
        # response = self.client.put('/api/tesoreria/pago/aceptar/6/')
        # print(f'response JSON ===>>> 409 no tiene permitido pagar \n {json.dumps(response.data)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        
        # self.assertEqual(Pago.objects.get(id=6).estatus, 3)
        # self.assertEqual(PorExamen.objects.get(id=6).isPagado, False)
        
        # print('\n PAGO A POR EXAMEN NO EXISTE EL REGISTRO EN TABLA porExamen')
        # Pago.objects.filter(id=6).update(externoId=666)
        # response = self.client.put('/api/tesoreria/pago/aceptar/6/')
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


class GetPagoFilteredListTest(APITestCase):
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
        Pago.objects.create(concepto='concepto', comprobante='archvivo', monto=999.99, nota='nota', estatus=1, tipo=99, externoId=3)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/tesoreria/pago/list/?medico=9&tipo=99&externoId=3')  # a ver
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/tesoreria/pago/list/?medico=9')  # a ver
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

