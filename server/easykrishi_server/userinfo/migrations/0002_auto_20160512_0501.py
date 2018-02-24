# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('device_id', models.TextField()),
                ('model', models.CharField(max_length=250)),
                ('index_id', models.IntegerField()),
                ('action_url', models.CharField(max_length=250)),
                ('action_method', models.CharField(max_length=100)),
                ('created_date', models.DateField(default=datetime.date.today)),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPeople',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('created_date', models.DateField(default=datetime.date.today)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='people',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='dob',
        ),
        migrations.AddField(
            model_name='people',
            name='create_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='created_user_reference', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='people',
            name='modified_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='modified_by_user_reference', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='peopleotherinformation',
            name='last_modified',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='user',
            name='last_modified',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userleaders',
            name='last_modified',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='otpverification',
            name='create_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='people',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='people',
            name='last_modified',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='peopleotherinformation',
            name='create_date',
            field=models.DateTimeField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userleaders',
            name='create_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='userpeople',
            name='people',
            field=models.ForeignKey(to='userinfo.People', related_name='people_user_reference'),
        ),
        migrations.AddField(
            model_name='userpeople',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='User_people_id'),
        ),
        migrations.AddField(
            model_name='actionlog',
            name='create_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='log_user_reference'),
        ),
    ]
