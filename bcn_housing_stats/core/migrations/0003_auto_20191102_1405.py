# Generated by Django 2.2.6 on 2019-11-02 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20191102_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcetype',
            name='slug',
            field=models.SlugField(choices=[('AVERAGE_MONTHLY_RENT', 'AVERAGE_MONTHLY_RENT')], max_length=100),
        ),
    ]
