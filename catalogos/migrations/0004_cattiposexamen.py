# Generated by Django 3.1.6 on 2021-02-16 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0003_auto_20210216_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatTiposExamen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'cat_tipos_examen',
            },
        ),
    ]