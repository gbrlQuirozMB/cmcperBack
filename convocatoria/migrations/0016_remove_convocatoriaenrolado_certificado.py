# Generated by Django 3.1.6 on 2021-04-05 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convocatoria', '0015_convocatoriaenrolado_isaprobado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convocatoriaenrolado',
            name='certificado',
        ),
    ]
