# Generated by Django 3.1.6 on 2021-02-09 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('company_name', models.CharField(max_length=128, unique=True)),
                ('paid_until', models.DateField(auto_now=True)),
                ('on_trial', models.BooleanField(default=True)),
                ('db_conf', models.JSONField()),
                ('db_name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
