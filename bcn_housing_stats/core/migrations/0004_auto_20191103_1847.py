# Generated by Django 2.2.6 on 2019-11-03 18:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20191102_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='file',
            field=models.FileField(blank=True, upload_to='data_uploads/%Y', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv', 'CSV'])]),
        ),
        migrations.AlterField(
            model_name='resource',
            name='url',
            field=models.URLField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='resourcetype',
            name='slug',
            field=models.SlugField(choices=[('AVERAGE_MONTHLY_RENT', 'AVERAGE_MONTHLY_RENT'), ('AVERAGE_OCCUPANCY', 'AVERAGE_OCCUPANCY')], max_length=100),
        ),
    ]