from django.core.validators import FileExtensionValidator
from django.db import models

from .managers import CustomResourceManager
from config.settings.base import ResourceTypeSLUGS


class ResourceType(models.Model):
    slug = models.SlugField(max_length=100, choices=ResourceTypeSLUGS.choices())
    name = models.CharField(max_length=200, verbose_name=u'Name')
    description = models.TextField(max_length=1000, verbose_name=u'Description')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.slug}'


class Resource(models.Model):
    type = models.ForeignKey('ResourceType', on_delete=models.CASCADE)
    url = models.URLField(max_length=1000)
    file = models.FileField(upload_to='data_uploads/%Y', validators=[
        FileExtensionValidator(allowed_extensions=['csv', 'CSV'])])
    name = models.CharField(max_length=200, verbose_name=u'Name')
    description = models.TextField(max_length=1000, verbose_name=u'Description')
    year = models.PositiveSmallIntegerField(verbose_name=u'Year')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomResourceManager()

    def __str__(self):
        return f'{self.year} | {self.name} | {self.type.slug}'
