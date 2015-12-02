# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfm', '0009_auto_20151202_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='photo',
            field=models.ImageField(default=b'photos/default.png', null=True, upload_to=b'photos', blank=True),
        ),
    ]
