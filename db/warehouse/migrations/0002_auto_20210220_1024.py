# Generated by Django 3.1.6 on 2021-02-20 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehousestorage',
            name='unit_id',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
