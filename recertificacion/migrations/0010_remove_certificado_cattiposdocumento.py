# Generated by Django 3.1.6 on 2021-04-05 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recertificacion', '0009_auto_20210405_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificado',
            name='catTiposDocumento',
        ),
    ]
