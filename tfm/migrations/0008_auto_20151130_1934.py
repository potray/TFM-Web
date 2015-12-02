# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfm', '0007_auto_20151124_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='test_type',
            field=models.CharField(max_length=2, choices=[(b'SS', b'Simon says'), (b'SL', b'Straight line'), (b'ST', b'Simon says with a tool')]),
        ),
    ]
