# Generated by Django 3.1.6 on 2021-02-16 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='catsedes',
            name='direccion',
            field=models.CharField(default=str, max_length=200),
            preserve_default=False,
        ),
    ]