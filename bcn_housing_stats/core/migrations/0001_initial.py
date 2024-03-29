# Generated by Django 2.2.6 on 2019-11-02 13:48

import config.settings.base
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(choices=[(config.settings.base.ResourceTypeSLUGS('AVERAGE_MONTHLY_RENT'), 'AVERAGE_MONTHLY_RENT')])),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(max_length=1000, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=1000)),
                ('file', models.FileField(upload_to='data_uploads/%Y', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv', 'CSV'])])),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(max_length=1000, verbose_name='Description')),
                ('year', models.PositiveSmallIntegerField(verbose_name='Year')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ResourceType')),
            ],
        ),
    ]
