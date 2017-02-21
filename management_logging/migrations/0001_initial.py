# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logging',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('class_name', models.CharField(max_length=150)),
                ('stdout_output', models.TextField()),
                ('stderr_output', models.TextField()),
                ('status', models.CharField(max_length=10)),
                ('start_datetime', models.DateTimeField(auto_now_add=True)),
                ('finish_datetime', models.DateTimeField(null=True, blank=True)),
            ],
        )
    ]
