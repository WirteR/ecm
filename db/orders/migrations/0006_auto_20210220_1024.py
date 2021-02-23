# Generated by Django 3.1.6 on 2021-02-20 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0001_initial'),
        ('orders', '0005_auto_20210216_2223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseorder',
            name='invoice',
        ),
        migrations.RemoveField(
            model_name='salesorder',
            name='invoice',
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='invoices',
            field=models.ManyToManyField(blank=True, related_name='purchase_orders', to='orders.Invoice'),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='invoices',
            field=models.ManyToManyField(blank=True, related_name='sale_orders', to='orders.Invoice'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='url',
            field=models.FileField(upload_to='invoice'),
        ),
        migrations.AlterField(
            model_name='productunit',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='creditor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_orders', to='payment.account'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_orders', to='payment.payment'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sellers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='user_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='debitor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sale_orders', to='payment.account'),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sale_orders', to='payment.payment'),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='user_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sale_orders', to=settings.AUTH_USER_MODEL),
        ),
    ]