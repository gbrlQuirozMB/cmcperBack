# Generated by Django 3.1.6 on 2021-08-25 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0004_auto_20210706_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatEntidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entidad', models.CharField(max_length=50)),
                ('region', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'cat_entidad',
            },
        ),
    ]