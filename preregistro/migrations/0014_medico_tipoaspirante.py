# Generated by Django 3.1.6 on 2021-09-21 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preregistro', '0013_medico_regiongeografica'),
    ]

    operations = [
        migrations.AddField(
            model_name='medico',
            name='tipoAspirante',
            field=models.CharField(choices=[('Normal', 'Normal'), ('Extemporaneo', 'Extemporaneo'), ('Especial', 'Especial')], default='---', max_length=15),
        ),
    ]
