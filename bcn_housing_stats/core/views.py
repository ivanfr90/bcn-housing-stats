from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from config.settings.base import ResourceTypeSLUGS
from .models import Resource
from .services import AverageRentalPriceService, AverageOccupancyService, AverageTouristOccupancyService


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = 2018

        # years = Resource.objects.get_years_by_resource_type(
        #     ResourceTypeSLUGS.AVERAGE_MONTHLY_RENT.value).values_list('year', flat=True)
        # AverageRentalPriceService.initialize_data(years=years, offset=200)
        # categories, value_list = AverageRentalPriceService.get_average_rentals()
        # average = AverageRentalPriceService.get_total_average_rental()

        # years = Resource.objects.get_years_by_resource_type(
        #     ResourceTypeSLUGS.AVERAGE_OCCUPANCY.value).values_list('year', flat=True)
        # AverageOccupancyService.initialize_data(years=years, offset=200)
        # categories, value_list = AverageOccupancyService.get_average_occupancy()
        # average = None

        years = Resource.objects.get_years_by_resource_type(
            ResourceTypeSLUGS.AVERAGE_TOURIST_OCCUPANCY.value).values_list('year', flat=True)
        AverageTouristOccupancyService.initialize_data(years=years, offset=200)
        categories, value_list = AverageTouristOccupancyService.get_average_occupancy()
        average = None

        context['categories'] = categories # json.dumps(props, default=json_serial)
        context['value_list'] = value_list
        context['average_rental'] = average
        context['year'] = year
        return context

class Dashboard(TemplateView):
    template_name = "core/dashboard.html"


home_view = HomeView.as_view()
dashboard_view = Dashboard.as_view()
