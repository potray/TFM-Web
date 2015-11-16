# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfm', '0002_auto_20151116_1209'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tfmuser',
            old_name='user_password',
            new_name='password',
        ),
        migrations.RemoveField(
            model_name='tfmuser',
            name='user_name',
        ),
        migrations.AddField(
            model_name='tfmuser',
            name='email',
            field=models.CharField(default='none', max_length=100),
            preserve_default=False,
        ),
    ]
