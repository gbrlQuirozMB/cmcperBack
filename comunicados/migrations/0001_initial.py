# Generated by Django 3.1.6 on 2021-05-10 15:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comunicado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('titulo', models.CharField(max_length=300)),
                ('categoria', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Categoria 1'), (2, 'Categoria 2'), (3, 'Categoria 3')])),
                ('imagen', models.FileField(blank=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif'])])),
                ('detalles', models.TextField(blank=True)),
                ('isActivo', models.BooleanField(db_column='is_activo', default=False)),
            ],
            options={
                'db_table': 'comunicados',
                'ordering': ['-actualizado_en'],
            },
        ),
    ]