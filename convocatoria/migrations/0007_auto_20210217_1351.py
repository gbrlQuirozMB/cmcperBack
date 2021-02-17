# Generated by Django 3.1.6 on 2021-02-17 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0004_cattiposexamen'),
        ('convocatoria', '0006_auto_20210215_1000'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sede',
            options={'ordering': ['-catSedes']},
        ),
        migrations.AlterModelOptions(
            name='tipoexamen',
            options={'ordering': ['-catTiposExamen']},
        ),
        migrations.RenameField(
            model_name='convocatoria',
            old_name='actualzado_en',
            new_name='actualizado_en',
        ),
        migrations.RemoveField(
            model_name='sede',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='tipoexamen',
            name='descripcion',
        ),
        migrations.AddField(
            model_name='sede',
            name='catSedes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='catSedes', to='catalogos.catsedes'),
        ),
        migrations.AddField(
            model_name='tipoexamen',
            name='catTiposExamen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='catTiposExamen', to='catalogos.cattiposexamen'),
        ),
        migrations.AlterField(
            model_name='tipoexamen',
            name='convocatoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tiposExamen', to='convocatoria.convocatoria'),
        ),
    ]