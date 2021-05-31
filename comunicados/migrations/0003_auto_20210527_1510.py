# Generated by Django 3.1.6 on 2021-05-27 20:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunicados', '0002_auto_20210514_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comunicado',
            name='imagen',
            field=models.FileField(blank=True, upload_to='comunicados', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif', 'jpeg'])]),
        ),
    ]
