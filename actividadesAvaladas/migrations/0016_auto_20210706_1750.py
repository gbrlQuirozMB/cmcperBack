# Generated by Django 3.1.6 on 2021-07-06 22:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividadesAvaladas', '0015_auto_20210623_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividadavalada',
            name='banner',
            field=models.FileField(blank=True, upload_to='actividadesAvaladas', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'gif', 'jpeg'])]),
        ),
    ]
