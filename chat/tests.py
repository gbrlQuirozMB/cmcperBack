from notificaciones.models import Notificacion
from rest_framework.test import APITestCase
from .models import *
from preregistro.models import *
from rest_framework import status
import json

nl = '\n'


# Create your tests here.
class baseDatosTest(APITestCase):
    def setUp(self):
        Mensaje.objects.create(mensaje='mensaje1',destinatario=111,remitente=369)
        Mensaje.objects.create(mensaje='mensaje2',destinatario=222,remitente=369)
        Mensaje.objects.create(mensaje='mensaje3',destinatario=333,remitente=369)
        Conversacion.objects.create(nombre='nombre1',destinatario=111)
        Conversacion.objects.create(nombre='nombre2',destinatario=222)
        Conversacion.objects.create(nombre='nombre3',destinatario=333)
    
    def test(self):
        # crear mensaje nuevo
        Mensaje.objects.create(mensaje='mensajeX',destinatario=222,remitente=369)
        Conversacion.objects.filter(destinatario=222).delete()
        Conversacion.objects.create(nombre='nombreX',destinatario=222)
        
        queryset = Mensaje.objects.filter(remitente=369)
        print(queryset)
        # print(f'{queryset.query} {nl} --- {nl}')
        for dato in queryset:
            print(f'mensaje: {dato.mensaje}')
        
        queryset2 = Conversacion.objects.all()    
        print(queryset2)
        for dato in queryset2:
            print(f'conversacion: {dato.nombre}')
            
            
class Post201Test(APITestCase):
    def setUp(self):
        Mensaje.objects.create(mensaje='mensaje1',destinatario=111,remitente=369)
        Mensaje.objects.create(mensaje='mensaje2',destinatario=222,remitente=369)
        Mensaje.objects.create(mensaje='mensaje3',destinatario=333,remitente=369)
        Conversacion.objects.create(nombre='nombre1',destinatario=111)
        Conversacion.objects.create(nombre='nombre2',destinatario=222)
        Conversacion.objects.create(nombre='nombre3',destinatario=333)
        Medico.objects.create(nombre='n1', apPaterno='app1', apMaterno='apm1', rfc='rfc1', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1', deleMuni='deleMuni1',
                        colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1', cedEspecialidad='cedEspecialidad1',
                        cedCirugiaGral='cedCirugiaGral1',hospitalResi='hospitalResi1',telJefEnse='telJefEnse1',fechaInicioResi='1999-06-06',fechaFinResi='2000-07-07',telCelular='telCelular1',
                        telParticular='telParticular1',email='email1', numRegistro=222)
        self.json = {
            "mensaje": "mesaje del json",
            "destinatario": 222,
            "remitente": 369
        }
        
    def test(self):
        
        conSesion = False #True-> mandamos variable de sesion para poner en la DB, False-> como no existe la sesion se obtiene de la DB y se pone en sesion
        
        if conSesion:
            sesion = self.client.session
            sesion["nombre"] = 'gabriel quiroz'
            sesion.save()
        
        response = self.client.post('/api/chat/create/', data=self.json)
        print(f'response JSON ===>>> {nl} {response.data} {nl} ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conversacion.objects.count(), 3) # debe ser 3 porque se borra el que existe
        
        if conSesion:
            self.assertEqual(Conversacion.objects.get(id=4).nombre, 'gabriel quiroz') # regresa el nombre concatenado para mostrarte en la lista
        else:
            self.assertEqual(Conversacion.objects.get(id=4).nombre, 'n1 app1 apm1') # regresa el nombre concatenado para mostrarte en la lista
        
         # que la notificaion este correcta
        queryset = Notificacion.objects.all()
        for dato in queryset:
            print(f'--->>>dato: titulo: {dato.titulo}, mensaje: {dato.mensaje}, destinatario: {dato.destinatario}, remitente: {dato.remitente}')
            
            
class GetChatList200Test(APITestCase):
    def setUp(self):
        Medico.objects.create(nombre='n1', apPaterno='app1', apMaterno='apm1', rfc='rfc1', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1', deleMuni='deleMuni1',
                colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1', cedEspecialidad='cedEspecialidad1',
                cedCirugiaGral='cedCirugiaGral1',hospitalResi='hospitalResi1',telJefEnse='telJefEnse1',fechaInicioResi='1999-06-06',fechaFinResi='2000-07-07',telCelular='telCelular1',
                telParticular='telParticular1',email='email1', numRegistro=333)
        self.json = {
            "mensaje": "mesaje del json",
            "destinatario": 333,
            "remitente": 369
        }
        self.jsonOtro = {
            "mensaje": "mesaje del json",
            "destinatario": 333,
            "remitente": 111
        }
    def test(self):
        self.client.post('/api/chat/create/', data=self.json)
        self.client.post('/api/chat/create/', data=self.json)
        self.client.post('/api/chat/create/', data=self.json)
        self.client.post('/api/chat/create/', data=self.json)
        self.client.post('/api/chat/create/', data=self.json)
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        
        response = self.client.get('/api/chat/all/369/333/')
        print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')

        response = self.client.get(
            '/api/chat/all/369/333/?size=3&page=1&orderby=id&direc=asc')
        print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')

        response = self.client.get(
            '/api/chat/all/369/333/?size=3&page=2&orderby=id&direc=asc')
        print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        

class GetConversacionList200Test(APITestCase):
    def setUp(self):
        Medico.objects.create(nombre='n1', apPaterno='app1', apMaterno='apm1', rfc='rfc1', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1', deleMuni='deleMuni1',
                colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1', cedEspecialidad='cedEspecialidad1',
                cedCirugiaGral='cedCirugiaGral1',hospitalResi='hospitalResi1',telJefEnse='telJefEnse1',fechaInicioResi='1999-06-06',fechaFinResi='2000-07-07',telCelular='telCelular1',
                telParticular='telParticular1',email='email1', numRegistro=333, fotoPerfil='mi_foto_333.png')
        Medico.objects.create(nombre='n2', apPaterno='app2', apMaterno='apm2', rfc='rfc2', curp='curp2', fechaNac='2020-09-09', pais='pais2', estado='estado2', ciudad='ciudad2', deleMuni='deleMuni2',
                colonia='colonia', calle='calle2', cp='cp2', numExterior='numExterior2', rfcFacturacion='rfcFacturacion2', cedProfesional='cedProfesional2', cedEspecialidad='cedEspecialidad2',
                cedCirugiaGral='cedCirugiaGral2',hospitalResi='hospitalResi2',telJefEnse='telJefEnse2',fechaInicioResi='1999-06-06',fechaFinResi='2000-07-07',telCelular='telCelular2',
                telParticular='telParticular2',email='email2', numRegistro=666, fotoPerfil='mi_foto_666.png')
        self.json = {
            "mensaje": "mesaje del json",
            "destinatario": 333,
            "remitente": 369
        }
        self.jsonOtro = {
            "mensaje": "mesaje del json",
            "destinatario": 666,
            "remitente": 369
        }
    def test(self):
        sesion = self.client.session
        sesion["nombre"] = 'gabriel quiroz'
        sesion.save()
        self.client.post('/api/chat/create/', data=self.json)
        self.client.post('/api/chat/create/', data=self.json)
        self.client.post('/api/chat/create/', data=self.json)
        self.client.post('/api/chat/create/', data=self.json)
        self.client.post('/api/chat/create/', data=self.json)
        sesion["nombre"] = 'luis enrique'
        sesion.save()
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        
        response = self.client.get('/api/chat/conversaciones/')
        print(f'response JSON ===>>> {nl} {json.dumps(response.json())} {nl} ---')

        # response = self.client.get(
        #     '/api/chat/conversaciones/?size=3&page=1')
        # print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')

        # response = self.client.get(
        #     '/api/chat/conversaciones/?size=3&page=2')
        # print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        

class GetMedicoChatList200Test(APITestCase):
    def setUp(self):
            Medico.objects.create(id=1, nombre='n1', apPaterno='app1', apMaterno='apm1', rfc='rfc1', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1', deleMuni='deleMuni1',
                                colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1', cedEspecialidad='cedEspecialidad1',
                                cedCirugiaGral='cedCirugiaGral1',hospitalResi='hospitalResi1',telJefEnse='telJefEnse1',fechaInicioResi='1999-06-06',fechaFinResi='2000-07-07',telCelular='telCelular1',
                                telParticular='telParticular1',email='email1',aceptado=True,numRegistro=333, fotoPerfil='mi_foto_333.png')
            Medico.objects.create(id=2, nombre='n2', apPaterno='app2', apMaterno='apm2', rfc='rfc2', curp='curp2', fechaNac='2020-09-09', pais='pais2', estado='estado2', ciudad='ciudad2', deleMuni='deleMuni2',
                                colonia='colonia', calle='calle2', cp='cp2', numExterior='numExterior2', rfcFacturacion='rfcFacturacion2', cedProfesional='cedProfesional2', cedEspecialidad='cedEspecialidad2',
                                cedCirugiaGral='cedCirugiaGral2',hospitalResi='hospitalResi2',telJefEnse='telJefEnse2',fechaInicioResi='1999-06-06',fechaFinResi='2000-07-07',telCelular='telCelular2',
                                telParticular='telParticular2',email='email2',aceptado=True,numRegistro=666, fotoPerfil='mi_foto_666.png')
            Medico.objects.create(id=3, nombre='n3', apPaterno='app3', apMaterno='apm3', rfc='rfc3', curp='curp3', fechaNac='2020-09-09', pais='pais3', estado='estado3', ciudad='ciudad3', deleMuni='deleMuni3',
                                colonia='colonia', calle='calle3', cp='cp3', numExterior='numExterior3', rfcFacturacion='rfcFacturacion3', cedProfesional='cedProfesional3', cedEspecialidad='cedEspecialidad3',
                                cedCirugiaGral='cedCirugiaGral3',hospitalResi='hospitalResi3',telJefEnse='telJefEnse3',fechaInicioResi='1999-06-06',fechaFinResi='2000-07-07',telCelular='telCelular3',
                                telParticular='telParticular3',email='email3',aceptado=True,numRegistro=999, fotoPerfil='mi_foto_999.png')

    def test(self):
        response = self.client.get('/api/chat/medicos/list/')
        print(f'response JSON ===>>> {nl} {json.dumps(response.json())} {nl} ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)