# Generated by Django 3.1.6 on 2021-06-03 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividadesAvaladas', '0008_auto_20210531_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asistenteactividadavalada',
            name='qrCodeImg',
        ),
    ]
