# Generated by Django 3.1.6 on 2021-02-18 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0005_auto_20210218_1216'),
        ('convocatoria', '0009_auto_20210218_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convocatoriaenroladodocumento',
            name='catTiposDocumento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catTiposDocumentoD', to='catalogos.cattiposdocumento'),
        ),
    ]
