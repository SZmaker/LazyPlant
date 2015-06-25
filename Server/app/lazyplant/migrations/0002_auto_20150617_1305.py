# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lazyplant', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='iotrecord',
            options={'verbose_name': 'IoT Record', 'verbose_name_plural': 'IoT Records'},
        ),
    ]
