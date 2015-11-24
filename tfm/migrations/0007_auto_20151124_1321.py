# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfm', '0006_auto_20151124_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='photo',
            field=models.ImageField(default=b'photos/default.png', upload_to=b'photos', blank=True),
        ),
    ]
