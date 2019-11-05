from rest_framework import serializers

from .models import Resource, ResourceType


class ResourceTypeSerializerReduced(serializers.ModelSerializer):

    class Meta:
        model = ResourceType
        fields = ('id', 'slug')

class ResourceSerializer(serializers.ModelSerializer):
    # type = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    type = ResourceTypeSerializerReduced(read_only=True)

    class Meta:
        model = Resource
        fields = ('id', 'type_id', 'type', 'url', 'file', 'name', 'description', 'year')
