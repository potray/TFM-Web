# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tfm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_type', models.CharField(max_length=2, choices=[(b'SS', b'Simon says'), (b'SL', b'Straight line')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('result', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TfmUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=200)),
                ('user_name', models.CharField(max_length=50)),
                ('user_password', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('tfmuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tfm.TfmUser')),
                ('specialization', models.CharField(max_length=100)),
            ],
            bases=('tfm.tfmuser',),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('tfmuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tfm.TfmUser')),
                ('description', models.TextField()),
                ('sex', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('doctor', models.ForeignKey(to='tfm.Doctor')),
            ],
            bases=('tfm.tfmuser',),
        ),
        migrations.AddField(
            model_name='testresult',
            name='patient',
            field=models.ForeignKey(to='tfm.Patient'),
        ),
    ]
