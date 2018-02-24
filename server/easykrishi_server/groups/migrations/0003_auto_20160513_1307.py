# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_auto_20160512_0501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmember',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='productbuyingdetails',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 13, 13, 7, 52, 390209, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productsellingdetails',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 13, 13, 7, 56, 78278, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
