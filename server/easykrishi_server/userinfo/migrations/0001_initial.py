# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('mobile_number', models.CharField(unique=True, max_length=45)),
                ('aadhar_number', models.CharField(unique=True, max_length=45)),
                ('first_name', models.CharField(blank=True, null=True, max_length=100)),
                ('last_name', models.CharField(blank=True, null=True, max_length=45)),
                ('dob', models.DateField(blank=True, null=True)),
                ('address', models.CharField(blank=True, null=True, max_length=45)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', to='auth.Group', related_query_name='user', blank=True, related_name='user_set')),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', verbose_name='user permissions', to='auth.Permission', related_query_name='user', blank=True, related_name='user_set')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
        ),
        migrations.CreateModel(
            name='Otpverification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('mobile_number', models.CharField(max_length=25)),
                ('otp_number', models.CharField(max_length=100)),
                ('is_verified', models.BooleanField(default=False)),
                ('create_date', models.DateField()),
                ('expired_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('mobile_number', models.CharField(max_length=150)),
                ('aadhar_number', models.CharField(blank=True, null=True, max_length=150)),
                ('first_name', models.CharField(blank=True, null=True, max_length=100)),
                ('last_name', models.CharField(blank=True, null=True, max_length=100)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('house_number', models.CharField(blank=True, null=True, max_length=20)),
                ('village', models.CharField(blank=True, null=True, max_length=100)),
                ('sub_district_or_mandal', models.CharField(blank=True, null=True, max_length=100)),
                ('district', models.CharField(blank=True, null=True, max_length=100)),
                ('city_name', models.CharField(blank=True, null=True, max_length=100)),
                ('state_name', models.CharField(blank=True, null=True, max_length=100)),
                ('country_name', models.CharField(blank=True, null=True, max_length=100)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(blank=True, null=True)),
                ('last_modified', models.DateTimeField(blank=True, null=True)),
                ('is_synced', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Peopleotherinformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('key', models.CharField(max_length=250)),
                ('value', models.CharField(max_length=250)),
                ('create_date', models.DateTimeField(blank=True, null=True)),
                ('create_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, db_column='create_by')),
                ('people', models.ForeignKey(to='userinfo.People')),
            ],
        ),
        migrations.CreateModel(
            name='Userleaders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('create_date', models.DateField()),
                ('leader', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_related_to_leader')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user_related_to_user')),
            ],
        ),
    ]
