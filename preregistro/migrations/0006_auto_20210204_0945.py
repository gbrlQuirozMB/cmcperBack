# Generated by Django 3.1.6 on 2021-02-04 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preregistro', '0005_auto_20210202_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='medico',
            name='razonSocial',
            field=models.CharField(blank=True, db_column='razon_social', max_length=250),
        ),
        migrations.AlterField(
            model_name='medico',
            name='usoCfdi',
            field=models.CharField(choices=[('G03', 'Gastos en General'), ('P01', 'Por Definir')], db_column='uso_cfdi', default='P01', max_length=5),
        ),
    ]
