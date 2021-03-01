# Generated by Django 3.1.6 on 2021-02-24 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20210224_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesorder',
            name='bookkeeping_status',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='marketplace',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='shipment_label',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='shipment_service',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='shipping_price',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
    ]
