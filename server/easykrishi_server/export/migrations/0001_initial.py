# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0007_auto_20160615_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderedProducts',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('groups.productbuyingdetails',),
        ),
        migrations.CreateModel(
            name='SellProducts',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('groups.productsellingdetails',),
        ),
    ]
