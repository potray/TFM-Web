# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfm', '0002_testresult_is_new'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='description',
            new_name='history',
        ),
    ]
