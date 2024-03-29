# Generated by Django 3.1.6 on 2021-06-25 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instituciones', '0002_institucion_username'),
        ('tesoreria', '0004_auto_20210531_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='institucion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institucionP', to='instituciones.institucion'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='tipo',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
