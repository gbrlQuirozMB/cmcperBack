# Generated by Django 3.1.6 on 2022-01-17 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entregaFisica', '0002_auto_20220117_1425'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entregafisica',
            old_name='fecha',
            new_name='fechaEntrega',
        ),
    ]