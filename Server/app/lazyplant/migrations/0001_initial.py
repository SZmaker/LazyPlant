# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IoTRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('co2', models.FloatField(null=True, blank=True)),
                ('o2', models.FloatField(null=True, blank=True)),
                ('humidity', models.FloatField(null=True, blank=True)),
                ('temperature', models.FloatField(null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'iotimages', blank=True)),
                ('timestamp', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
