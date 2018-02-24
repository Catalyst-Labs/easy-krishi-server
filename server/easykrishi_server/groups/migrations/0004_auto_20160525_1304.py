# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_auto_20160513_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbuyingdetails',
            name='measurement',
            field=models.CharField(max_length=100, default='unit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productsellingdetails',
            name='measurement',
            field=models.CharField(max_length=100, default='unit'),
            preserve_default=False,
        ),
    ]
