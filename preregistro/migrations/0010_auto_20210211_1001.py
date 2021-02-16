# Generated by Django 3.1.6 on 2021-02-11 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preregistro', '0009_auto_20210210_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='medico',
            name='escuelaExtranjero',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='medico',
            name='estudioExtranjero',
            field=models.BooleanField(db_column='estudio_extranjero', default=False),
        ),
    ]