# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tourn', '0003_auto_20141128_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teamentry',
            name='players',
            field=models.ManyToManyField(related_name=b'tournament_entries', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
