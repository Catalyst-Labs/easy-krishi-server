# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0005_auto_20160526_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmember',
            name='offline_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productbuyingdetails',
            name='offline_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productsellingdetails',
            name='offline_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='offline_id',
            field=models.BigIntegerField(default=0),
        ),
    ]
