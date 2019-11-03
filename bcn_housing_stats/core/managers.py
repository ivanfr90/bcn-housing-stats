from django.db import models
from django.db.models import Q


class ResourceQuerySet(models.QuerySet):

    def get_years_by_resource_type_query(self, type):
        args = [Q(type__slug=type)]
        sort_fields = ['-year']
        qs = self.filter(*args).order_by(*sort_fields)
        return qs

class CustomResourceManager(models.Manager):
    def get_queryset(self):
        return ResourceQuerySet(self.model, using=self._db)

    def get_years_by_resource_type(self, type):
        return self.get_queryset().get_years_by_resource_type_query(type)
