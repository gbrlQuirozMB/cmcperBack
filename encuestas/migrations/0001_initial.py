# Generated by Django 3.1.6 on 2022-02-04 21:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('preregistro', '0017_auto_20211220_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.CharField(max_length=200)),
                ('fechaInicio', models.DateField(db_column='fecha_inicio', default=datetime.date.today)),
                ('fechaFin', models.DateField(db_column='fecha_fin', default=datetime.date.today)),
                ('estatus', models.CharField(choices=[('Editar', 'Editar'), ('Abierta', 'Abierta'), ('Cerrada', 'Cerrada')], default='Editar', max_length=15)),
                ('regionGeografica', models.CharField(blank=True, db_column='region_geografica', max_length=300)),
                ('isSoloConsejero', models.BooleanField(db_column='is_solo_consejero', default=False)),
            ],
            options={
                'db_table': 'encuestas',
                'ordering': ['-creado_en'],
            },
        ),
        migrations.CreateModel(
            name='Opcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
                ('orden', models.PositiveSmallIntegerField()),
            ],
            options={
                'db_table': 'opciones',
                'ordering': ['orden'],
            },
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
                ('orden', models.PositiveSmallIntegerField()),
                ('hasOtro', models.BooleanField(db_column='acepta_otro', default=False)),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuestas.encuesta')),
            ],
            options={
                'db_table': 'preguntas',
                'ordering': ['orden'],
            },
        ),
        migrations.CreateModel(
            name='Respuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('otro', models.CharField(blank=True, max_length=200, null=True)),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuestas.encuesta')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preregistro.medico')),
                ('opcion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='encuestas.opcion')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuestas.pregunta')),
            ],
            options={
                'db_table': 'respuestas',
                'ordering': ['-creado_en'],
            },
        ),
        migrations.AddField(
            model_name='opcion',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuestas.pregunta'),
        ),
    ]
