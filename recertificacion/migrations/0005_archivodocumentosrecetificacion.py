# Generated by Django 3.1.6 on 2021-07-29 17:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('preregistro', '0007_medico_iscertificado'),
        ('recertificacion', '0004_auto_20210706_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivoDocumentosRecetificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('documento', models.FileField(blank=True, upload_to='recertificacion', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif', 'jpeg'])])),
                ('tituloDescripcion', models.CharField(db_column='titulo_descripcion', max_length=300)),
                ('fechaEmision', models.DateField(db_column='fecha_emision')),
                ('puntosOtorgados', models.DecimalField(db_column='puntos_otorgados', decimal_places=2, max_digits=6)),
                ('estatus', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Aceptado'), (2, 'Rechazado'), (3, 'Pendiente')])),
                ('observaciones', models.TextField(blank=True, db_column='observaciones')),
                ('notasRechazo', models.TextField(blank=True, db_column='notas_rechzo')),
                ('razonRechazo', models.CharField(blank=True, db_column='razon_rechazo', max_length=200)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemADR', to='recertificacion.item')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicoADR', to='preregistro.medico')),
            ],
            options={
                'db_table': 'archivo_documentos_recertificacion',
                'ordering': ['-actualizado_en'],
            },
        ),
    ]