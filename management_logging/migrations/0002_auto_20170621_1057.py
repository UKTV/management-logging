# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management_logging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='logging',
            name='site',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='logging',
            name='stderr_output',
            field=models.TextField(verbose_name=b'Error output'),
        ),
        migrations.AlterField(
            model_name='logging',
            name='stdout_output',
            field=models.TextField(verbose_name=b'Output'),
        ),
    ]
