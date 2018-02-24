# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0007_auto_20160624_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormKeysInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('key', models.CharField(max_length=250)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('create_by', models.ForeignKey(db_column='create_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FormsInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('create_by', models.ForeignKey(db_column='create_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PeopleKeysDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('offline_id', models.BigIntegerField(default=0)),
                ('value', models.TextField(blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('create_by', models.ForeignKey(db_column='create_by', to=settings.AUTH_USER_MODEL)),
                ('form', models.ForeignKey(related_name='people_forms_keys', to='userinfo.FormsInformation')),
                ('people', models.ForeignKey(to='userinfo.People')),
            ],
        ),
        migrations.RemoveField(
            model_name='extrakeysinformation',
            name='create_by',
        ),
        migrations.RemoveField(
            model_name='peopleextrainformation',
            name='create_by',
        ),
        migrations.RemoveField(
            model_name='peopleextrainformation',
            name='key',
        ),
        migrations.RemoveField(
            model_name='peopleextrainformation',
            name='people',
        ),
        migrations.DeleteModel(
            name='ExtraKeysInformation',
        ),
        migrations.DeleteModel(
            name='PeopleExtrainformation',
        ),
        migrations.AddField(
            model_name='formkeysinformation',
            name='form',
            field=models.ForeignKey(related_name='forms_keys', to='userinfo.FormsInformation'),
        ),
    ]
