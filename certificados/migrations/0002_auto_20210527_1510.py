# Generated by Django 3.1.6 on 2021-05-27 20:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificados', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificado',
            name='documento',
            field=models.FileField(blank=True, upload_to='certificados', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif'])]),
        ),
    ]
