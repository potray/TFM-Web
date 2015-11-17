# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('specialization', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(default=b'', max_length=100)),
                ('last_name', models.CharField(default=b'', max_length=200)),
                ('description', models.TextField()),
                ('sex', models.BooleanField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('doctor', models.ForeignKey(to='tfm.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_type', models.CharField(max_length=2, choices=[(b'SS', b'Simon says'), (b'SL', b'Straight line')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('result', models.TextField()),
                ('patient', models.ForeignKey(to='tfm.Patient')),
            ],
        ),
    ]
