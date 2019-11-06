from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from config.settings.base import ResourceTypeSLUGS
from .models import Resource
from .services import RentalPriceService, AverageResidentsService, TouristRentalsService


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
        # AverageResidentsService.initialize_data(years=years, offset=200)
        # categories, value_list = AverageResidentsService.get_average_occupancy()
        # average = None

        years = Resource.objects.get_years_by_resource_type(
            ResourceTypeSLUGS.AVERAGE_TOURIST_OCCUPANCY.value).values_list('year', flat=True)
        TouristRentalsService.initialize_data(years=years, offset=200)
        categories, value_list = TouristRentalsService.get_average_occupancy()
        average = None

        context['categories'] = categories # json.dumps(props, default=json_serial)
        context['value_list'] = value_list
        context['average_rental'] = average
        context['year'] = year
        return context

class DashBoardView(TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        years = Resource.objects.all().values_list('year', flat=True).distinct().order_by('-year')
        context['years'] = years
        return context


home_view = HomeView.as_view()
dashboard_view = DashBoardView.as_view()
