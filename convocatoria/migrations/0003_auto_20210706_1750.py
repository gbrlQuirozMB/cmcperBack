# Generated by Django 3.1.6 on 2021-07-06 22:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convocatoria', '0002_auto_20210527_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convocatoria',
            name='banner',
            field=models.FileField(blank=True, upload_to='convocatoria', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'gif', 'jpeg'])]),
        ),
        migrations.AlterField(
            model_name='convocatoriaenroladodocumento',
            name='documento',
            field=models.FileField(blank=True, upload_to='convocatoria', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif', 'jpeg'])]),
        ),
    ]
