# Generated by Django 3.1.6 on 2021-07-06 22:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0003_auto_20210527_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catsedes',
            name='imagen',
            field=models.FileField(blank=True, null=True, upload_to='catalogos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg', 'gif', 'jpeg'])]),
        ),
    ]
