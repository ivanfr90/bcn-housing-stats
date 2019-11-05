import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.base import ResourceTypeSLUGS
from .models import Resource, ResourceType
from .serializers import ResourceSerializer, ResourceTypeSerializer
from .services import (
    AverageTouristOccupancyService,
    AverageRentalPriceService,
    AverageOccupancyService)

logger = logging.getLogger(__name__)


class ResourceTypeAPI(APIView):

    def get(self, request, pk):
        logger.info('ResourceTypeAPI GET called')
        try:
            resource_type = ResourceType.objects.get(pk=pk)
        except ResourceType.DoesNotExist as e:
            logger.info('Resource Type does not exists', exc_info=True, extra={'exception': e})
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ResourceTypeSerializer(resource_type)
        return Response(serializer.data)

class ResourceTypeListAPI(APIView):

    def get(self, request):
        logger.info('ResourceTypeListAPI GET called')
        resources_types = ResourceType.objects.all()
        serializer = ResourceTypeSerializer(resources_types, many=True)
        return Response(serializer.data)

class ResourceAPI(APIView):

    def get(self, request, pk):
        logger.info('ResourceAPI GET called')
        try:
            resource = Resource.objects.get(pk=pk)
        except Resource.DoesNotExist as e:
            logger.info('Resource does not exists', exc_info=True, extra={'exception': e})
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ResourceSerializer(resource)
        return Response(serializer.data)


class ResourceListAPI(APIView):

    def get(self, request):
        logger.info('ResourceListAPI GET called')
        resources = Resource.objects.all().order_by('type__slug', 'year')
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)


class ResourceDataAPI(APIView):

    def get(self, request, resource_type_pk):
        logger.info('ResourceDataAPI GET called')
        try:
            years_param = self.request.query_params.get('years', None)
            type_slug = ResourceType.objects.get(pk=resource_type_pk).slug

            categories = []
            series = []
            custom_data = {}
            if years_param:
                years = [int(item) for item in years_param.split(',')]
            else:
                years = Resource.objects.get_years_by_resource_type(type_slug).values_list('year', flat=True)

            if type_slug == ResourceTypeSLUGS.AVERAGE_MONTHLY_RENT.value:
                AverageRentalPriceService.initialize_data(years=years, offset=200)
                categories, series = AverageRentalPriceService.get_average_rentals()
                average_per_years = AverageRentalPriceService.get_total_average_rental()
                custom_data = {'average_per_years': average_per_years}
            elif type_slug == ResourceTypeSLUGS.AVERAGE_OCCUPANCY.value:
                AverageOccupancyService.initialize_data(years=years, offset=200)
                categories, series = AverageOccupancyService.get_average_occupancy()
            elif type_slug == ResourceTypeSLUGS.AVERAGE_TOURIST_OCCUPANCY.value:
                AverageTouristOccupancyService.initialize_data(years=years, offset=200)
                categories, series = AverageTouristOccupancyService.get_average_occupancy()
        except ResourceType.DoesNotExist as e:
            logger.info('ResourceData does not exists', exc_info=True, extra={'exception': e})
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            logger.info('Invalid year', exc_info=True, extra={'exception': e})
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({
            'categories': categories,
            'series': series,
            **custom_data
        })
