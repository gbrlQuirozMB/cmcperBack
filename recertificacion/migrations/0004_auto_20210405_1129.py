# Generated by Django 3.1.6 on 2021-04-05 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recertificacion', '0003_auto_20210402_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capitulo',
            name='maximo',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='capitulo',
            name='minimo',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='capitulo',
            name='puntos',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
