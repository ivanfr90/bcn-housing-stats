import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings.base import ResourceTypeSLUGS
from .models import Resource, ResourceType
from .serializers import ResourceSerializer, ResourceTypeSerializer, AverageRentalPriceSerializer, \
    AverageResidentsSerializer, TouristOccupancySerializer
from .services import (
    TouristRentalsService,
    RentalPriceService,
    AverageResidentsService)

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
            flat = self.request.query_params.get('flat', None)
            type_slug = ResourceType.objects.get(pk=resource_type_pk).slug

            if years_param:
                years = [int(item) for item in years_param.split(',')]
            else:
                years = Resource.objects.get_years_by_resource_type(type_slug).values_list('year', flat=True)

            data_response = {}
            if type_slug == ResourceTypeSLUGS.AVERAGE_MONTHLY_RENT.value:
                RentalPriceService.initialize_data(years=years, offset=200)
                if not flat:
                    categories, series = RentalPriceService.get_average_rentals()
                    data_response.update({'average_rental': {
                        'categories': categories,
                        'series': series
                    }})
                    categories, series = RentalPriceService.get_average_rental_by_years()
                    data_response.update({'average_rental_per_years': {
                        'categories': categories,
                        'series': series
                    }})
                else:
                    serializer = AverageRentalPriceSerializer(RentalPriceService.get_plain_data(), many=True)
                    data_response = {'data': serializer.data}
            elif type_slug == ResourceTypeSLUGS.AVERAGE_OCCUPANCY.value:
                AverageResidentsService.initialize_data(years=years, offset=200)
                if not flat:
                    categories, series = AverageResidentsService.get_average_residents()
                    data_response.update({'average_residents': {
                        'categories': categories,
                        'series': series
                    }})
                    categories, series = AverageResidentsService.get_residents_per_year()
                    data_response.update({'residents_per_years': {
                        'categories': categories,
                        'series': series
                    }})
                else:
                    serializer = AverageResidentsSerializer(AverageResidentsService.get_plain_data(), many=True)
                    data_response = {'data': serializer.data}
            elif type_slug == ResourceTypeSLUGS.TOURIST_OCCUPANCY.value:
                TouristRentalsService.initialize_data(years=years, offset=200)
                if not flat:
                    categories, series = TouristRentalsService.get_average_rentals_neighborhood()
                    data_response.update({'tourist_rental_per_neighborhood': {
                        'categories': categories,
                        'series': series
                    }})
                    categories, series = TouristRentalsService.get_rentals_accommodations_per_years()
                    data_response.update({'tourist_rentals_per_years': {
                        'categories': categories,
                        'series': series
                    }})
                    values = TouristRentalsService.get_average_rentals_grouped_district()
                    data_response.update({'tourist_rental_accommodations_per_years': values})
                else:
                    serializer = TouristOccupancySerializer(TouristRentalsService.get_plain_data(), many=True)
                    data_response = {'data': serializer.data}
        except ResourceType.DoesNotExist as e:
            logger.info('ResourceData does not exists', exc_info=True, extra={'exception': e})
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            logger.info('Invalid year', exc_info=True, extra={'exception': e})
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(data_response)
