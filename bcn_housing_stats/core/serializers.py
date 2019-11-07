from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField, FloatField

from .models import Resource, ResourceType


class ResourceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResourceType
        fields = ('id', 'slug', 'name', 'description')

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

class AverageRentalPriceSerializer(serializers.Serializer):

    concept = CharField()
    code_district = IntegerField()
    name_district = CharField()
    code_neighborhood = IntegerField()
    name_neighborhood = CharField()
    quarter = IntegerField()
    price = FloatField()
    year = IntegerField()

    class Meta:
        model = Resource
        fields = ('concept', 'code_district', 'name_district', 'code_neighborhood', 'name_neighborhood', 'quarter', 'price', 'year')


class AverageResidentsSerializer(serializers.Serializer):

    code_district = IntegerField()
    name_district = CharField()
    code_neighborhood = IntegerField()
    name_neighborhood = CharField()
    houses = IntegerField()
    residents = IntegerField()
    average_occupancy = FloatField()
    year = IntegerField()

    class Meta:
        model = Resource
        fields = ('code_district', 'name_district', 'code_neighborhood', 'name_neighborhood', 'houses', 'residents', 'average_occupancy', 'year')


class TouristOccupancySerializer(serializers.Serializer):

    name_district = CharField()
    name_neighborhood = CharField()
    accommodation_type = CharField()
    price = FloatField()
    availability = IntegerField()

    class Meta:
        model = Resource
        fields = ('name_district', 'name_neighborhood', 'accommodation_type', 'price', 'availability')
