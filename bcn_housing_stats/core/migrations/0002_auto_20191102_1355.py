# Generated by Django 2.2.6 on 2019-11-02 13:55

import config.settings.base
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcetype',
            name='slug',
            field=models.SlugField(choices=[(config.settings.base.ResourceTypeSLUGS('AVERAGE_MONTHLY_RENT'), 'AVERAGE_MONTHLY_RENT')], max_length=5),
        ),
    ]
