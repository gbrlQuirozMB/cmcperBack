# Generated by Django 3.1.6 on 2021-11-09 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preregistro', '0015_auto_20211102_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='medico',
            name='titulo',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
    ]
