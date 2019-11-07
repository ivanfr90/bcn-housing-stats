from django.views.generic import TemplateView

from config.settings.base import ResourceTypeSLUGS
from .models import Resource, ResourceType
from .services import RentalPriceService, AverageResidentsService, TouristRentalsService

class DashBoardView(TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        years = Resource.objects.all().values_list('year', flat=True).distinct().order_by('-year')
        context['years'] = years
        return context


class DataTablesView(TemplateView):
    template_name = "core/datatables.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resource_types = ResourceType.objects.all()

        data = []
        for resource_type in resource_types:
            if resource_type.slug == ResourceTypeSLUGS.AVERAGE_MONTHLY_RENT.value:
                RentalPriceService.initialize_data()
                categories = ['Concept', 'Disctrict Code', 'District Name', 'Neighborhood Code', 'Neighborhood Name',
                              'Quarter', 'Price', 'year']
                values = []
                for plain_data in RentalPriceService.get_plain_data():
                    value = []

                    value.append(plain_data.concept)
                    value.append(plain_data.code_district)
                    value.append(plain_data.name_district)
                    value.append(plain_data.code_neighborhood)
                    value.append(plain_data.name_neighborhood)
                    value.append(plain_data.quarter)
                    value.append(plain_data.price)
                    value.append(plain_data.year)

                    values.append(value)

                data.append({
                    'resource': resource_type,
                    'columns': categories,
                    'values': values
                })
            elif resource_type.slug == ResourceTypeSLUGS.AVERAGE_OCCUPANCY.value:
                AverageResidentsService.initialize_data()
                categories = ['Disctrict Code', 'District Name', 'Neighborhood Code', 'Neighborhood Name',
                              'Houses', 'Residents', 'Average Occupancy', 'year']
                values = []
                for plain_data in AverageResidentsService.get_plain_data():
                    value = []
                    value.append(plain_data.code_district)
                    value.append(plain_data.name_district)
                    value.append(plain_data.code_neighborhood)
                    value.append(plain_data.name_neighborhood)
                    value.append(plain_data.houses)
                    value.append(plain_data.residents)
                    value.append(plain_data.average_occupancy)
                    value.append(plain_data.year)

                    values.append(value)

                data.append({
                    'resource': resource_type,
                    'columns': categories,
                    'values': values
                })
            # elif resource_type.slug == ResourceTypeSLUGS.TOURIST_OCCUPANCY.value:
            #     TouristRentalsService.initialize_data()
            #     categories = ['District Name', 'Neighborhood Name',
            #                   'Accommodation Type', 'Price', 'Availability']
            #     values = []
            #     for plain_data in TouristRentalsService.get_plain_data():
            #         value = []
            #         value.append(plain_data.name_district)
            #         value.append(plain_data.name_neighborhood)
            #         value.append(plain_data.accommodation_type)
            #         value.append(plain_data.price)
            #         value.append(plain_data.availability)
            #
            #         values.append(value)
            #
            #     data.append({
            #         'resource': resource_type,
            #         'columns': categories,
            #         'values': values
            #     })

        context['resource_types'] = resource_types
        context['data'] = data
        return context

dashboard_view = DashBoardView.as_view()
datatables_view = DataTablesView.as_view()
