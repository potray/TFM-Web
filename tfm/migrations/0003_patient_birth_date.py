# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tfm', '0002_auto_20151117_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='birth_date',
            field=models.DateField(default=datetime.datetime(2015, 11, 17, 17, 10, 21, 10000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
