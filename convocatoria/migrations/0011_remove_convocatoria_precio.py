# Generated by Django 3.1.6 on 2021-02-25 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convocatoria', '0010_auto_20210218_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convocatoria',
            name='precio',
        ),
    ]
