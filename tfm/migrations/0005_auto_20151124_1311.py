# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfm', '0004_auto_20151124_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='photo',
            field=models.ImageField(default=None, upload_to=b'photos', blank=True),
            preserve_default=False,
        ),
    ]
