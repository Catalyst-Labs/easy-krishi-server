# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0006_auto_20160601_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productbuyingdetails',
            name='product_image',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='productsellingdetails',
            name='product_image',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
