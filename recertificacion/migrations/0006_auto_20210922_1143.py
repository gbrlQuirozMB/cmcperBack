# Generated by Django 3.1.6 on 2021-09-22 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recertificacion', '0005_archivodocumentosrecetificacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='porexamen',
            name='calificacion',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]