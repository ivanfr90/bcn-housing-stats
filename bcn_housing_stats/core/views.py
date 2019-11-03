from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from config.settings.base import ResourceTypeSLUGS
from .models import Resource
from .services import AverageRentalPriceService


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = 2018

        years = Resource.objects.get_years_by_resource_type(
            ResourceTypeSLUGS.AVERAGE_MONTHLY_RENT.value).values_list('year', flat=True)

        categories, value_list = AverageRentalPriceService.get_all_average_rentals(years=years, offset=200)
        # categories, value_list = AverageRentalPriceService.get_average_rental(2014)

        average = None #AverageRentalPriceService.get_total_average_rental()

        context['categories'] = categories # json.dumps(props, default=json_serial)
        context['value_list'] = value_list
        context['average_rental'] = average
        context['year'] = year
        return context

home_view = HomeView.as_view()
