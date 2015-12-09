# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visit_doctor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name="Client's name"),
        ),
    ]
