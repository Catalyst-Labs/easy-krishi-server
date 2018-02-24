# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import groups.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userinfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groupmember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, blank=True, null=True)),
                ('created_date', models.DateField(blank=True, null=True)),
                ('create_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, db_column='create_by')),
                ('member', models.ForeignKey(to='userinfo.People')),
            ],
        ),
        migrations.CreateModel(
            name='Productbuyingdetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('product_name', models.CharField(max_length=200)),
                ('product_image', models.ImageField(blank=True, upload_to=groups.models.set_unique_image_for_buy)),
                ('product_qty', models.CharField(max_length=100, blank=True, null=True)),
                ('product_price', models.FloatField(blank=True, null=True)),
                ('alternate_address', models.CharField(max_length=250, blank=True, null=True)),
                ('create_date', models.DateField()),
                ('last_modified', models.DateTimeField(blank=True, null=True)),
                ('product_required_date', models.DateField(blank=True, null=True)),
                ('people', models.ForeignKey(to='userinfo.People')),
            ],
        ),
        migrations.CreateModel(
            name='Productsellingdetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('product_name', models.CharField(max_length=200)),
                ('product_image', models.ImageField(blank=True, upload_to=groups.models.set_unique_image_for_sell)),
                ('product_qty', models.CharField(max_length=100)),
                ('product_price', models.FloatField()),
                ('product_harvest_date', models.DateField()),
                ('alternate_address', models.CharField(max_length=250, blank=True, null=True)),
                ('create_date', models.DateField()),
                ('last_modified', models.DateTimeField(blank=True, null=True)),
                ('people', models.ForeignKey(to='userinfo.People')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('created_date', models.DateField()),
                ('create_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='created_user', db_column='create_by')),
                ('leader', models.ForeignKey(related_name='group_leader', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='productsellingdetails',
            name='user_group',
            field=models.ForeignKey(to='groups.UserGroup'),
        ),
        migrations.AddField(
            model_name='productbuyingdetails',
            name='user_group',
            field=models.ForeignKey(to='groups.UserGroup'),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='user_group',
            field=models.ForeignKey(to='groups.UserGroup'),
        ),
    ]
