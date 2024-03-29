# Generated by Django 3.1.6 on 2021-05-18 15:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recertificacion', '0002_renovacion'),
        ('instituciones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActividadAvalada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('nombre', models.CharField(max_length=200)),
                ('emailContacto', models.CharField(db_column='email_contacto', max_length=50)),
                ('archivo', models.FileField(blank=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])])),
                ('banner', models.FileField(blank=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'gif'])])),
                ('numAsistentes', models.PositiveSmallIntegerField(db_column='numero_asistentes')),
                ('puntosAsignar', models.DecimalField(db_column='puntos_asignar', decimal_places=2, max_digits=6)),
                ('fechaInicio', models.DateField(db_column='fecha_inicio')),
                ('lugar', models.CharField(max_length=300)),
                ('solicitante', models.CharField(max_length=300)),
                ('tipoPago', models.PositiveSmallIntegerField(choices=[(1, 'Porcentaje'), (2, 'Precio')], db_column='tipo_pago')),
                ('porcentaje', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=7, null=True)),
                ('descripcion', models.TextField(blank=True)),
                ('institucion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institucionA', to='instituciones.institucion')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemA', to='recertificacion.item')),
            ],
            options={
                'db_table': 'actividades_avaladas',
                'ordering': ['-creado_en'],
            },
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=300)),
                ('actividadAvalada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividadAvaladaT', to='actividadesAvaladas.actividadavalada')),
            ],
            options={
                'db_table': 'temas',
                'ordering': ['-nombre'],
            },
        ),
    ]
