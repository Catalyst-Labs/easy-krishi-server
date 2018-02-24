# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0004_auto_20160525_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='productbuyingdetails',
            name='user',
            field=models.ForeignKey(related_name='user_people_buy_product', default=6, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productsellingdetails',
            name='user',
            field=models.ForeignKey(related_name='user_people_sell_product', default=6, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
