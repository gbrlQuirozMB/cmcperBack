# Generated by Django 3.1.6 on 2021-05-19 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividadesAvaladas', '0003_auto_20210518_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividadavalada',
            name='isPagado',
            field=models.BooleanField(db_column='is_pagado', default=False),
        ),
    ]
