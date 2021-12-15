# from dateutil import relativedelta
from dateutil.relativedelta import relativedelta

from .models import *

from django.test import TestCase
from preregistro.models import Medico
from certificados.models import Certificado
from rest_framework.test import APITestCase
from datetime import date
from rest_framework import status
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import json

from django.db.models.functions import Concat, TruncMonth, Extract


def configDB(self):
    self.medico3 = Medico.objects.create(
        id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2023-03-03', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=333, diplomaConacem='Pone Dora', titulo='Dra.')
    self.medico6 = Medico.objects.create(
        id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2026-06-06', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=666, diplomaConacem='GlandM Enormes', titulo='Dra.')
    self.medico9 = Medico.objects.create(
        id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2029-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999, diplomaConacem='Yo mero', titulo='Dr.')
    self.medico5 = Medico.objects.create(
        id=5, nombre='grissel', apPaterno='bejarano', apMaterno='islas', rfc='quog??0406', curp='curp1', fechaNac='2025-05-05', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999, diplomaConacem='XXX', titulo='Dr.')

    Certificado.objects.create(medico=self.medico3, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                               fechaCaducidad=date.today()+relativedelta(years=5), estatus=1, documento='ya_hay_algo.pdf', isConacem=False)
    Certificado.objects.create(medico=self.medico3, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                               fechaCaducidad=date.today()+relativedelta(years=5), estatus=2, documento='ya_hay_algo.pdf', isConacem=True)
    Certificado.objects.create(medico=self.medico9, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                               fechaCaducidad=date.today()+relativedelta(years=5), estatus=1, documento='ya_hay_algo.pdf', isConacem=False)
    Certificado.objects.create(medico=self.medico3, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                               fechaCaducidad=date.today()+relativedelta(years=5), estatus=2, documento='ya_hay_algo.pdf', isConacem=True)
    Certificado.objects.create(medico=self.medico6, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                               fechaCaducidad=date.today()+relativedelta(years=5), estatus=1, documento='ya_hay_algo.pdf', isConacem=False)
    Certificado.objects.create(medico=self.medico5, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                               fechaCaducidad=date.today()+relativedelta(years=5), estatus=3, documento='ya_hay_algo.pdf', isConacem=True)


class GetConacemMedicosListTest(APITestCase):
    def setUp(self):
        configDB(self)
        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/conacem/medicos/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostConacemTest(APITestCase):
    def setUp(self):
        configDB(self)

        self.json = {
            "fechaEnvio": "2021-04-06",
            "tituloPresidente": "dactar",
            "nombrePresidente": "gabriel quiroz",
            "tituloResponsable": "enferm",
            "nombreResponsable": "elianid tolentino",
            "fechaEmision": "2021-04-06",
            "costo": 369.33,
            "fechaValidezDel": "2021-04-06",
            "fechaValidezAl": "2021-04-06",
            "iniciaLibro": 3,
            "hoja": 3,
            "lugar": 6,
            "cupo": 9,
            "medicos": [
                {"medico": 3},
                {"medico": 6},
                {"medico": 9}
            ]
            # "medicos":[]
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):

        self.client.force_authenticate(user=self.user)

        # para revisar como esta el estatus 'isConacem' de los certificados antes
        for datoCertificado in Certificado.objects.filter().order_by('id'):
            print(f'--->>>datoCertificado.id: {datoCertificado.id} -- datoCertificado.medico.id: {datoCertificado.medico.id} -- datoCertificado.isConacem: {datoCertificado.isConacem}')

        response = self.client.post('/api/conacem/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # del self.json['nombreInstitucion']
        # response = self.client.post('/api/conacem/create/', data=json.dumps(self.json), content_type="application/json")
        # print(f'response JSON ===>>> ok \n {json.dumps(response.data)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # para revisar que este bien el libro y foja en detalles
        datosDetalle = DetalleConcacem.objects.filter()
        if datosDetalle.count() > 0:
            for dato in datosDetalle:
                print(f'--->>>detalle.medico.id: {dato.medico.id} --- libro: {dato.libro} --- foja: {dato.foja} --- detalle.nombre: {dato.medico.nombre} --- detalle.conacem.id: {dato.conacem.id}')

        # para revisar como esta el estatus 'isConacem' de los certificados antes
        print(f'\n')
        for datoCertificado in Certificado.objects.filter().order_by('id'):
            print(f'--->>>datoCertificado.id: {datoCertificado.id} -- datoCertificado.medico.id: {datoCertificado.medico.id} -- datoCertificado.isConacem: {datoCertificado.isConacem}')


def configDBConacem(self):
    conacem1 = Conacem.objects.create(
        fechaEnvio='2021-04-06', tituloPresidente='Dactar', nombrePresidente='gabriel quiroz', tituloResponsable='enferm', nombreResponsable='elianid tolentino', fechaEmision='2021-04-06',
        costo=369.33, fechaValidezDel='2021-04-06', fechaValidezAl='2021-04-06', iniciaLibro=3, hoja=3, lugar=6, cupo=9)
    conacem2 = Conacem.objects.create(
        fechaEnvio='2021-04-06', tituloPresidente='Dactar', nombrePresidente='laura vargas', tituloResponsable='enferm', nombreResponsable='grissel bejarano tolentino', fechaEmision='2021-04-06',
        costo=369.33, fechaValidezDel='2021-04-06', fechaValidezAl='2021-04-06', iniciaLibro=3, hoja=3, lugar=6, cupo=9)
    DetalleConcacem.objects.create(medico=self.medico3, conacem=conacem1, libro=3, foja=6, observaciones='ninguna', numCertificado=33)
    DetalleConcacem.objects.create(medico=self.medico6, conacem=conacem1, libro=3, foja=7, observaciones='ninguna', numCertificado=66)
    DetalleConcacem.objects.create(medico=self.medico9, conacem=conacem2, libro=3, foja=8, observaciones='ninguna', numCertificado=99)


class GetDescargarExcel200Test(APITestCase):
    def setUp(self):
        configDB(self)
        configDBConacem(self)

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/conacem/bajar-excel/1/list/')
        print(f'response JSON ===>>> ok \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/conacem/bajar-excel/3/list/')
        print(f'response JSON ===>>> ok \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # queryset = DetalleConcacem.objects.filter(conacem=1, medico__medicoC__isConacem=False).annotate(
        #     fNd=Extract('medico__fechaNac', 'day'),
        #     fNm=Extract('medico__fechaNac', 'month'),
        #     fNa=Extract('medico__fechaNac', 'year'),
        #     fEd=Extract('conacem__fechaEmision', 'day'),
        #     fEm=Extract('conacem__fechaEmision', 'month'),
        #     fEa=Extract('conacem__fechaEmision', 'year'),
        #     fVDd=Extract('conacem__fechaValidezDel', 'day'),
        #     fVDm=Extract('conacem__fechaValidezDel', 'month'),
        #     fVDa=Extract('conacem__fechaValidezDel', 'year'),
        #     fVAd=Extract('conacem__fechaValidezAl', 'day'),
        #     fVAm=Extract('conacem__fechaValidezAl', 'month'),
        #     fVAa=Extract('conacem__fechaValidezAl', 'year')).values_list('medico__titulo', 'medico__nombre', 'medico__apPaterno', 'medico__apMaterno', 'medico__hospitalResi',
        #                                                                  'medico__hospitalResi', 'medico__hospLaborPrim', 'medico__hospLaborSec', 'medico__rfc', 'medico__curp',
        #                                                                  'medico__cedProfesional', 'fNd', 'fNm', 'fNa', 'medico__nacionalidad', 'medico__estado', 'medico__deleMuni', 'medico__sexo',
        #                                                                  'fEd', 'fEm', 'fEa', 'fVDd', 'fVDm', 'fVDa', 'fVAd', 'fVAm', 'fVAa', 'medico__medicoC__id', 'libro', 'foja',
        #                                                                  'conacem__tituloPresidente','conacem__nombrePresidente','conacem__tituloResponsable','conacem__nombreResponsable',
        #                                                                  'conacem__costo','medico__email','observaciones','medico__cedEspecialidad')

        # queryset = DetalleConcacem.objects.filter(conacem=conacemId).values_list('medico__titulo', 'medico__nombre', 'medico__apPaterno', 'medico__apMaterno', 'medico__hospitalResi',
        #                                                                              'medico__hospitalResi','medico__hospLaborPrim','medico__hospLaborSec','medico__rfc')

        # for dato in queryset:
        #     print(f'dato: {dato}')


class GetConacemListTest(APITestCase):
    def setUp(self):
        configDB(self)
        configDBConacem(self)

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/conacem/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetDetalleConacemDetailTest(APITestCase):
    def setUp(self):
        configDB(self)
        configDBConacem(self)

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/conacem/1/detail/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PruebaTest(APITestCase):
    def setUp(self):
        pass

    def test(self):
        hoja = 6
        lugar = 9
        cupo = 12
        tam = 29

        quedan = (cupo-lugar)
        bandera = True
        for reg in range(tam):
            print(f'--->>>reg: {reg} -- hoja: {hoja} --- lugar: {lugar}')
            lugar = lugar + 1

            if lugar > cupo:
                # print(f'--->>>BANDERA-2: {bandera} -- hoja: {hoja} --- lugar: {lugar}')
                lugar = 1
                hoja = hoja + 1

        nombre = 'gabriel quiroz olvera'
        nada = nombre.split(' ')[0]
        print(f'--->>>nada: {nada}')
