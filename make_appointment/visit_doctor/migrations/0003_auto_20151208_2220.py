# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visit_doctor', '0002_auto_20151208_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='first_name',
            field=models.CharField(verbose_name="Client's first name", max_length=30),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='last_name',
            field=models.CharField(verbose_name="Client's last name", max_length=30),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='patronic_name',
            field=models.CharField(verbose_name="Client's patronic name", max_length=30),
        ),
    ]
