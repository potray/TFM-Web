# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfm', '0008_auto_20151130_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('diary_straight_line', models.IntegerField(default=-1)),
                ('diary_simon_says_hand', models.IntegerField(default=-1)),
                ('diary_simon_says_tool', models.IntegerField(default=-1)),
                ('simon_says_hand_max_hooks', models.IntegerField(default=5)),
                ('simon_says_tool_max_hooks', models.IntegerField(default=5)),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='settings',
            field=models.ForeignKey(default=None, to='tfm.PatientSettings'),
            preserve_default=False,
        ),
    ]
