# Generated by Django 3.1.6 on 2021-06-03 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividadesAvaladas', '0009_remove_asistenteactividadavalada_qrcodeimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividadavalada',
            name='qrCodeImg',
            field=models.ImageField(blank=True, upload_to='qr-codes'),
        ),
    ]
