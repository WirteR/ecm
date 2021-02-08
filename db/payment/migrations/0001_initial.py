# Generated by Django 3.1.5 on 2021-02-07 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('account_number', models.CharField(max_length=128)),
                ('account_type', models.CharField(max_length=64)),
                ('split_profit', models.DecimalField(decimal_places=2, max_digits=7)),
                ('account_cost', models.DecimalField(decimal_places=2, max_digits=7)),
                ('account_profit', models.DecimalField(decimal_places=2, max_digits=7)),
                ('default_for', models.CharField(max_length=64)),
                ('default_year', models.CharField(max_length=6)),
                ('online_account', models.CharField(max_length=128)),
                ('paypal_email', models.EmailField(max_length=128)),
                ('opening_date', models.DateField(auto_now=True)),
                ('translations', models.ManyToManyField(null=True, related_name='accounts', to='account.Translation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=24)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('note', models.CharField(max_length=128)),
                ('marketplace_id', models.CharField(max_length=128)),
                ('bookkeeping_status', models.CharField(max_length=64)),
                ('is_locked', models.BooleanField(default=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='payment.account')),
                ('translations', models.ManyToManyField(null=True, related_name='payments', to='account.Translation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]