# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0002_auto_20160512_0501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionlog',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='is_synced',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='peopleotherinformation',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userleaders',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userpeople',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
