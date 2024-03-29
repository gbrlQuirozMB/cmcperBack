# Generated by Django 3.1.6 on 2021-08-11 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preregistro', '0010_auto_20210811_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='medico',
            name='diplomaConacem',
            field=models.CharField(blank=True, db_column='diploma_conacem', max_length=300),
        ),
        migrations.AddField(
            model_name='medico',
            name='hospLaborPrim',
            field=models.CharField(blank=True, db_column='hosp_labora_primario', max_length=300),
        ),
        migrations.AddField(
            model_name='medico',
            name='hospLaborSec',
            field=models.CharField(blank=True, db_column='hosp_labora_secundario', max_length=300),
        ),
        migrations.AddField(
            model_name='medico',
            name='isConsultaPrivada',
            field=models.BooleanField(db_column='is_consulta_privada', default=False),
        ),
        migrations.AddField(
            model_name='medico',
            name='isExpresidente',
            field=models.BooleanField(db_column='is_expresidente', default=False),
        ),
        migrations.AddField(
            model_name='medico',
            name='isExprofesor',
            field=models.BooleanField(db_column='is_exprofesor', default=False),
        ),
        migrations.AddField(
            model_name='medico',
            name='isFinado',
            field=models.BooleanField(db_column='is_finado', default=False),
        ),
        migrations.AddField(
            model_name='medico',
            name='isRetirado',
            field=models.BooleanField(db_column='is_retirado', default=False),
        ),
        migrations.AddField(
            model_name='medico',
            name='titularHospital',
            field=models.CharField(blank=True, db_column='titular_hospital', max_length=300),
        ),
        migrations.AddField(
            model_name='medico',
            name='univEgreso',
            field=models.CharField(blank=True, db_column='universidad_egreso', max_length=300),
        ),
    ]
