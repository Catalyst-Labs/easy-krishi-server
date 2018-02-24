# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0005_auto_20160601_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpverification',
            name='mobile_number',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='people',
            name='mobile_number',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.BigIntegerField(unique=True),
        ),
    ]
