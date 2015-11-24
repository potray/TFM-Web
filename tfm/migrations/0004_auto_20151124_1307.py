# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfm', '0003_auto_20151124_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'photos'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='sex',
            field=models.BooleanField(max_length=1, choices=[(True, b'Male'), (False, b'Female')]),
        ),
    ]
