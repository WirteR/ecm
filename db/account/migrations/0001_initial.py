# Generated by Django 3.1.6 on 2021-03-09 22:03

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('street', models.CharField(max_length=256)),
                ('street_number', models.CharField(blank=True, default=True, max_length=16)),
                ('zip', models.CharField(max_length=24)),
                ('city', models.CharField(max_length=64)),
                ('country', models.CharField(blank=True, default='', max_length=64)),
                ('key', models.CharField(blank=True, max_length=128, null=True)),
                ('location_name', models.CharField(blank=True, max_length=128, null=True)),
                ('location_ID', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(max_length=24)),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=128, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=128, null=True)),
                ('avatar', models.ImageField(null=True, upload_to='user-avatars')),
                ('lang', models.CharField(default='en-GB', max_length=16, null=True)),
                ('phone', models.CharField(max_length=24)),
                ('account', models.CharField(max_length=128, null=True)),
                ('street', models.CharField(max_length=256)),
                ('street_number', models.CharField(blank=True, default=True, max_length=16)),
                ('zip', models.CharField(max_length=24)),
                ('city', models.CharField(max_length=64)),
                ('country', models.CharField(blank=True, default='', max_length=64)),
                ('tenant_id', models.IntegerField()),
                ('groups', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.customergroup')),
                ('user_permissions', models.ManyToManyField(blank=True, to='account.CustomerPermission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
