# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0008_auto_20160627_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='device_information',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='userleaders',
            name='create_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userpeople',
            name='created_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
