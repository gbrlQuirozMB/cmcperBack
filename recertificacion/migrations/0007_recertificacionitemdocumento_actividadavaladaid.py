# Generated by Django 3.1.6 on 2021-10-01 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recertificacion', '0006_auto_20210922_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='recertificacionitemdocumento',
            name='actividadAvaladaId',
            field=models.PositiveSmallIntegerField(blank=True, db_column='actividad_avalada_id', null=True),
        ),
    ]
