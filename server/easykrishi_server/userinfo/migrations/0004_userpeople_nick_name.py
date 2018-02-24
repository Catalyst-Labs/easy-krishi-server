# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0003_auto_20160513_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpeople',
            name='nick_name',
            field=models.CharField(max_length=150, default='name'),
            preserve_default=False,
        ),
    ]
