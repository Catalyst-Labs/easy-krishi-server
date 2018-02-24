# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmember',
            name='last_modified',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='last_modified',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='groupmember',
            name='created_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='productbuyingdetails',
            name='create_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='productsellingdetails',
            name='create_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='created_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
