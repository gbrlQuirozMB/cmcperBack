# Generated by Django 3.1.6 on 2021-05-14 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preregistro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medico',
            name='facebook',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='medico',
            name='instagram',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='medico',
            name='linkedin',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='medico',
            name='pagWeb',
            field=models.CharField(blank=True, db_column='pag_web', max_length=300),
        ),
        migrations.AddField(
            model_name='medico',
            name='twitter',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='medico',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]