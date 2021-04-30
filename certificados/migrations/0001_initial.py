# Generated by Django 3.1.6 on 2021-04-30 15:05

import certificados.models
import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('preregistro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('documento', models.FileField(blank=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif'])])),
                ('descripcion', models.CharField(max_length=300)),
                ('isVencido', models.BooleanField(db_column='is_vencido', default=False)),
                ('fechaCertificacion', models.DateField(db_column='fecha_certificacion', default=datetime.date.today)),
                ('fechaCaducidad', models.DateField(db_column='fecha_caducidad', default=certificados.models.caducidad)),
                ('estatus', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Vigente'), (2, 'Esta por Vencer'), (3, 'Vencido')], default=1)),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicoC', to='preregistro.medico')),
            ],
            options={
                'db_table': 'certificados',
                'ordering': ['-actualizado_en'],
            },
        ),
    ]