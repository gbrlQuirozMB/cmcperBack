# Generated by Django 3.1.6 on 2021-05-31 22:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesoreria', '0003_auto_20210527_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='comprobante',
            field=models.FileField(blank=True, upload_to='tesoreria', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif', 'jpeg'])]),
        ),
    ]
