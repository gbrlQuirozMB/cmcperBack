# Generated by Django 3.1.6 on 2021-07-16 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preregistro', '0006_auto_20210706_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='medico',
            name='isCertificado',
            field=models.BooleanField(default=False),
        ),
    ]
