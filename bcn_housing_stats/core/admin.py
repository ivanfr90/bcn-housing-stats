from django.contrib import admin

from bcn_housing_stats.core.models import ResourceType, Resource

admin.site.register(ResourceType)
admin.site.register(Resource)
