# Generated by Django 3.1.6 on 2021-02-11 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='terms',
            field=models.TextField(null=True),
        ),
    ]
