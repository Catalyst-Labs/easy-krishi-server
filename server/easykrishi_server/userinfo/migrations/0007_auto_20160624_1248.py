# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0006_auto_20160602_1521'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extrakeysinformation',
            options={'verbose_name': 'Other Information', 'verbose_name_plural': 'Other Information'},
        ),
        migrations.AlterField(
            model_name='extrakeysinformation',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='people',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='people',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
    ]
