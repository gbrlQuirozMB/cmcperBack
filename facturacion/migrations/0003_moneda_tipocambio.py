# Generated by Django 3.1.6 on 2021-07-07 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0002_auto_20210624_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneda',
            name='tipoCambio',
            field=models.IntegerField(default=1),
        ),
    ]
