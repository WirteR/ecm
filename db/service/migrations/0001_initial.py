# Generated by Django 3.1.5 on 2021-02-07 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payment', '0001_initial'),
        ('orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now=True)),
                ('uid', models.CharField(max_length=64)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('bookkeeping_status', models.CharField(max_length=64)),
                ('is_locked', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExpenseFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=128)),
                ('url', models.FileField(upload_to='expense-files')),
                ('img', models.ImageField(upload_to='expense-image')),
                ('recource', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseSupplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('company_name', models.CharField(max_length=128)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supplier', to='payment.account')),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supplier', to='account.address')),
                ('supplier', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supplier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExpenseItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_items', to='service.expense')),
                ('translations', models.ManyToManyField(related_name='expense_items', to='account.Translation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExpenseCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('translations', models.ManyToManyField(related_name='expense_categories', to='account.Translation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='expense',
            name='expense_tag_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense', to='service.expensecategory'),
        ),
        migrations.AddField(
            model_name='expense',
            name='file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.expensefile'),
        ),
        migrations.AddField(
            model_name='expense',
            name='invoice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense', to='orders.invoice'),
        ),
        migrations.AddField(
            model_name='expense',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense', to='payment.payment'),
        ),
        migrations.AddField(
            model_name='expense',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense', to='service.expensesupplier'),
        ),
        migrations.AddField(
            model_name='expense',
            name='translations',
            field=models.ManyToManyField(related_name='expenses', to='account.Translation'),
        ),
    ]