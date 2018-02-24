# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0004_userpeople_nick_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraKeysInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('offline_id', models.BigIntegerField(default=0)),
                ('key', models.CharField(max_length=250)),
                ('create_date', models.DateTimeField(default=datetime.date.today)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('create_by', models.ForeignKey(db_column='create_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PeopleExtrainformation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('offline_id', models.BigIntegerField(default=0)),
                ('value', models.CharField(max_length=250)),
                ('create_date', models.DateTimeField(default=datetime.date.today)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('create_by', models.ForeignKey(db_column='create_by', to=settings.AUTH_USER_MODEL)),
                ('key', models.ForeignKey(related_name='key_value_relation', to='userinfo.ExtraKeysInformation')),
            ],
        ),
        migrations.RemoveField(
            model_name='peopleotherinformation',
            name='create_by',
        ),
        migrations.RemoveField(
            model_name='peopleotherinformation',
            name='people',
        ),
        migrations.AddField(
            model_name='people',
            name='offline_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userpeople',
            name='offline_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Peopleotherinformation',
        ),
        migrations.AddField(
            model_name='peopleextrainformation',
            name='people',
            field=models.ForeignKey(to='userinfo.People'),
        ),
    ]
