# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visit_doctor', '0004_auto_20151213_1244'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='doctor',
            unique_together=set([('first_name', 'last_name', 'patronic_name')]),
        ),
    ]
