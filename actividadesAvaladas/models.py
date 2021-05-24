from django.db import models
from django.core.validators import FileExtensionValidator

from instituciones.models import Institucion
from recertificacion.models import Item
from preregistro.models import Medico

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

import json

# Create your models here.


class ActividadAvalada(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name='institucionA')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='itemA')
    nombre = models.CharField(max_length=200)
    emailContacto = models.CharField(max_length=50, db_column='email_contacto')
    archivo = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    banner = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'gif'])])
    numAsistentes = models.PositiveSmallIntegerField(db_column='numero_asistentes')
    puntosAsignar = models.DecimalField(max_digits=6, decimal_places=2, db_column='puntos_asignar')
    fechaInicio = models.DateField(db_column='fecha_inicio')
    lugar = models.CharField(max_length=300)
    solicitante = models.CharField(max_length=300)
    tipoPago = models.PositiveSmallIntegerField(db_column='tipo_pago', choices=(
        (1, 'Porcentaje'),
        (2, 'Precio'),
    ))
    porcentaje = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    precio = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    descripcion = models.TextField(blank=True)
    isPagado = models.BooleanField(default=False, db_column='is_pagado')  # verificar si ya pago

    class Meta:
        db_table = 'actividades_avaladas'
        ordering = ['-creado_en']


class Tema(models.Model):
    nombre = models.CharField(max_length=300)
    # related no cumple con el nombre estandarizado ('actividadAvaladaT'), porque se utiliza en el serializer y llega hasta el json
    actividadAvalada = models.ForeignKey(ActividadAvalada, on_delete=models.CASCADE, related_name='temas')

    class Meta:
        db_table = 'temas'
        ordering = ['-nombre']


qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=6,
    border=3,
)


class AsistenteActividadAvalada(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medicoAAA')
    actividadAvalada = models.ForeignKey(ActividadAvalada, on_delete=models.CASCADE, related_name='actividadAvaladaAAA')
    qrCodeImg = models.ImageField(upload_to='qr-codes', blank=True)

    def save(self, *args, **kwargs):
        textoQr = {
            'medico': self.medico.id,
            # 'item': self.actividadAvalada.item.id,
            # 'fechaEmision': self.actividadAvalada.fechaInicio.strftime('%Y-%m-%d'),
            # 'puntosOtorgados': float(self.actividadAvalada.puntosAsignar)
            'actividadAvalada': self.actividadAvalada.id
        }
        qr.add_data(json.dumps(textoQr))
        qr.make(fit=True)
        qrcode_img = qr.make_image(fill_color="black", back_color="white")
        # canvas = Image.new('RGB', (233, 233), 'white')
        canvas = Image.new('RGB', (213, 212), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qrCode-M{self.medico.id}-AA{self.actividadAvalada.id}-I{self.actividadAvalada.item.id}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qrCodeImg.save(fname, File(buffer), save=False)
        qr.clear()
        super(AsistenteActividadAvalada, self).save(*args, **kwargs)

    class Meta:
        db_table = 'actividades_avaladas_asistentes'
        ordering = ['-actividadAvalada']
