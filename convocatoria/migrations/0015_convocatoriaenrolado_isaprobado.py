# Generated by Django 3.1.6 on 2021-04-01 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convocatoria', '0014_convocatoria_fecharesolucion'),
    ]

    operations = [
        migrations.AddField(
            model_name='convocatoriaenrolado',
            name='isAprobado',
            field=models.BooleanField(db_column='is_aprobado', default=False),
        ),
    ]
