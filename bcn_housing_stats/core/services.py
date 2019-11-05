import asyncio
import csv
import json
import logging
import time
from operator import itemgetter
from typing import Callable

from bcn_housing_stats.utils.utils import fetch_all_data
from config.settings.base import ResourceTypeSLUGS
from .constants import (
    AVG_RENTAL_PRICE_VALUE_CONCEPT_MONTHLY_RENTAL,
    AVG_RENTAL_PRICE,
    AVG_RENTAL_PRICE_VALUE_PRICE_NA,
    AVG_OCCUPANCY, AVG_TOURIST_OCCUPANCY)
from .models import Resource

logger = logging.getLogger(__name__)


class AverageRentalPrice:

    def __init__(self,
                 concept: str,
                 code_district: str,
                 name_district: str,
                 code_neighborhood: str,
                 name_neighborhood: str,
                 quarter: str,
                 price: str,
                 year: str):
        self.concept = concept
        self.code_district = int(code_district)
        self.name_district = name_district
        self.code_neighborhood = int(code_neighborhood)
        self.name_neighborhood = name_neighborhood
        self.quarter = int(quarter)
        self.price = float(price)
        self.year = int(year)


class AverageOccupancy:

    def __init__(self,
                 code_district: int,
                 name_district: str,
                 code_neighborhood: str,
                 name_neighborhood: str,
                 houses: str,
                 population: str,
                 average_occupancy: str,
                 year: str):
        self.code_district = int(code_district)
        self.name_district = name_district
        self.code_neighborhood = int(code_neighborhood)
        self.name_neighborhood = name_neighborhood
        self.houses = int(houses)
        self.population = int(population)
        self.average_occupancy = float(average_occupancy)
        self.year = int(year)

class AverageTouristOccupacy:

    def __init__(self,
                 name_district: str,
                 name_neighborhood: str,
                 accommodation_type: str="",
                 price: str="0",
                 availability: str= "0"
                 ):
        self.name_district = name_district
        self.name_neighborhood = name_neighborhood
        self.accommodation_type = accommodation_type
        self.price = float(price)
        self.availability = int(availability)
        self.average_occupancy = None



class AverageRentalPriceService:

    def __init__(self, years: list = [], offset: int = 100):
        self.years = years
        self.offset = offset
        self.data = []

    @classmethod
    def initialize_data(cls, years: list = [], offset: int = 100) -> None:
        cls(years, offset)
        if not years:
            year = Resource.objects.get_years_by_resource_type(
                ResourceTypeSLUGS.AVERAGE_MONTHLY_RENT.value).values_list('year', flat=True).order_by('-year').first()
            resources = Resource.objects.filter(
                type__slug=ResourceTypeSLUGS.AVERAGE_MONTHLY_RENT.value, year=year)
            cls.years = [resources.first().year] if resources else []
        else:
            resources = Resource.objects.filter(
                type__slug=ResourceTypeSLUGS.AVERAGE_MONTHLY_RENT.value, year__in=years).order_by("year")

        cls.data = []
        for resource in resources:
            start_time = time.time()
            if resource:
                data_transformed = []

                # first try from endpoint
                json_data_list = DataService.fetch_data(resource.url, offset)

                # if fails, try from csv file
                if json_data_list:
                    for json_data in json_data_list:
                        data_transformed += cls._transform_json_data(json_data)
                else:
                    dict_data_list = DataService.read_data(resource.file)
                    data_transformed = cls._transform_dict_data(dict_data_list)
                logger.info(f'Total transformed items {len(data_transformed)}')

                cls.data.append((resource.year, [*cls._unify_year_quarter_data(data_transformed)]))
                logger.info(f'Total unified items {len(cls.data)}')

            duration = time.time() - start_time
        print(f"Process time: {duration} seconds")

    @classmethod
    def get_average_rentals(cls) -> tuple:
        if not hasattr(cls, 'data'):
            raise Exception("Method initialize_data() not called. Class needs initialization")

        return DataService.normalize_data(
            cls.data,
            category_attr=lambda item: f'{getattr(item, "name_district")} / {getattr(item, "name_neighborhood")}',
            value_attr=lambda item: getattr(item, "price"))

    @classmethod
    def get_total_average_rental(cls) -> list:
        if not hasattr(cls, 'data'):
            raise Exception("Method initialize_data() not called. Class needs initialization")

        averages = []
        for year, data in cls.data:
            average_rental_values = data if data else []
            total = sum(item.price for item in average_rental_values)
            avg = total / len(average_rental_values)
            averages.append((year, avg))
        return averages

    @staticmethod
    def _transform_json_data(json_data: json) -> list:
        data = []
        if json_data and json_data['success'] is True:
            for record in json_data['result']['records']:
                empty_price = record[AVG_RENTAL_PRICE.PRICE] == AVG_RENTAL_PRICE_VALUE_PRICE_NA
                if not empty_price:
                    data.append(AverageRentalPriceService._create_object(record))
                else:
                    logger.warning(f'Element {record} with not price')
        return data

    @staticmethod
    def _transform_dict_data(dict_data_list: list) -> list:
        data = []
        for dict_data in dict_data_list:
            empty_price = dict_data[AVG_RENTAL_PRICE.PRICE] == AVG_RENTAL_PRICE_VALUE_PRICE_NA
            if not empty_price:
                data.append(AverageRentalPriceService._create_object(dict_data))
            else:
                logger.warning(f'Element {dict_data} with not price')
        return data

    @staticmethod
    def _create_object(dict_data: dict):
        try:
            average_rental_price = AverageRentalPrice(
                dict_data[AVG_RENTAL_PRICE.CONCEPT],
                dict_data[AVG_RENTAL_PRICE.DISTRICT_CODE],
                dict_data[AVG_RENTAL_PRICE.DISTRICT_NAME],
                dict_data[AVG_RENTAL_PRICE.NEIGHBORHOOD_CODE],
                dict_data[AVG_RENTAL_PRICE.NEIGHBORHOOD_NAME],
                dict_data[AVG_RENTAL_PRICE.QUARTER],
                dict_data[AVG_RENTAL_PRICE.PRICE],
                dict_data[AVG_RENTAL_PRICE.YEAR]
            )
            return average_rental_price
        except Exception as e:
            logger.error(f'An error reading transform data', exc_info=True, extra={'exception': e})

    @staticmethod
    def _unify_year_quarter_data(averages_rental_prices: list) -> list:
        """
        Unify year quarter data
        :param averages_rental_prices:
        :return:
        """
        # group all data by same district and neighborhood
        averages_rental_prices_dict = dict()
        for item in averages_rental_prices:
            key = f'{item.code_district}${item.code_neighborhood}${item.year}'
            monthly_rent_data = item.concept == AVG_RENTAL_PRICE_VALUE_CONCEPT_MONTHLY_RENTAL
            if key in averages_rental_prices_dict and monthly_rent_data:
                dict_items = averages_rental_prices_dict[key]
                dict_items.append(item)
            elif monthly_rent_data:
                averages_rental_prices_dict[key] = [item]

        # calculate the average monthly rent of each grouped list
        for key, average_rental_price_list in averages_rental_prices_dict.items():
            # average of quarter
            total = sum(item.price for item in average_rental_price_list)
            avg = total / len(average_rental_price_list)

            average_rental_price_list[0].prize = avg
            averages_rental_prices_dict[key] = average_rental_price_list[0]

        return averages_rental_prices_dict.values()


class AverageOccupancyService:

    def __init__(self, years: list = [], offset: int = 100):
        self.years = years
        self.offset = offset
        self.data = []

    @classmethod
    def initialize_data(cls, years: list = [], offset: int = 100) -> None:
        cls(years, offset)
        if not years:
            year = Resource.objects.get_years_by_resource_type(
                ResourceTypeSLUGS.AVERAGE_OCCUPANCY.value).values_list('year', flat=True).order_by('-year').first()
            resources = Resource.objects.filter(
                type__slug=ResourceTypeSLUGS.AVERAGE_OCCUPANCY.value, year=year)
            cls.years = [resources.first().year] if resources else []
        else:
            resources = Resource.objects.filter(
                type__slug=ResourceTypeSLUGS.AVERAGE_OCCUPANCY.value, year__in=years).order_by("year")

        cls.data = []
        for resource in resources:
            start_time = time.time()
            if resource:
                data_transformed = []

                # first try from endpoint
                json_data_list = DataService.fetch_data(resource.url, offset)

                # if fails, try from csv file
                if json_data_list:
                    for json_data in json_data_list:
                        data_transformed += cls._transform_json_data(json_data)
                else:
                    dict_data_list = DataService.read_data(resource.file)
                    data_transformed = cls._transform_dict_data(dict_data_list)
                logger.info(f'Total transformed items {len(data_transformed)}')

                cls.data.append((resource.year, data_transformed))
                logger.info(f'Total unified items {len(cls.data)}')

            duration = time.time() - start_time
        print(f"Process time: {duration} seconds")

    @classmethod
    def get_average_occupancy(cls) -> tuple:
        if not hasattr(cls, 'data'):
            raise Exception("Method initialize_data() not called. Class needs initialization")

        return DataService.normalize_data(
            cls.data,
            category_attr=lambda item: f'{getattr(item, "name_district")} / {getattr(item, "name_neighborhood")}',
            value_attr=lambda item: getattr(item, "population"))

    @staticmethod
    def _transform_json_data(json_data: json):
        data = []
        if json_data and json_data['success'] is True:
            for record in json_data['result']['records']:
                data.append(AverageOccupancyService._create_object(record))
        return data

    @staticmethod
    def _create_object(dict_data: dict):
        try:
            average_occupancy = AverageOccupancy(
                dict_data[AVG_OCCUPANCY.DISTRICT_CODE],
                dict_data[AVG_OCCUPANCY.DISTRICT_NAME],
                dict_data[AVG_OCCUPANCY.NEIGHBORHOOD_CODE],
                dict_data[AVG_OCCUPANCY.NEIGHBORHOOD_NAME],
                dict_data[AVG_OCCUPANCY.HOUSES],
                dict_data[AVG_OCCUPANCY.POPULATION],
                dict_data[AVG_OCCUPANCY.AVERAGE_OCCUPANCY],
                dict_data[AVG_OCCUPANCY.YEAR]
            )
            return average_occupancy
        except Exception as e:
            logger.error(f'An error reading transform data', exc_info=True, extra={'exception': e})



class AverageTouristOccupancyService:

    def __init__(self, years: list = [], offset: int = 100):
        self.years = years
        self.offset = offset
        self.data = []

    @classmethod
    def initialize_data(cls, years: list = [], offset: int = 100) -> None:
        cls(years, offset)
        if not years:
            year = Resource.objects.get_years_by_resource_type(
                ResourceTypeSLUGS.AVERAGE_TOURIST_OCCUPANCY.value).values_list('year', flat=True).order_by('-year').first()
            resources = Resource.objects.filter(
                type__slug=ResourceTypeSLUGS.AVERAGE_TOURIST_OCCUPANCY.value, year=year)
            cls.years = [resources.first().year] if resources else []
        else:
            resources = Resource.objects.filter(
                type__slug=ResourceTypeSLUGS.AVERAGE_TOURIST_OCCUPANCY.value, year__in=years).order_by("year")

        cls.data = []
        for resource in resources:
            start_time = time.time()
            if resource:
                data_transformed = []

                # first try from endpoint if has
                json_data_list = []
                if resource.url:
                    json_data_list = DataService.fetch_data(resource.url, offset)
                    for json_data in json_data_list:
                        data_transformed += cls._transform_json_data(json_data)
                elif resource.file and not json_data_list:
                    dict_data_list = DataService.read_data(resource.file)
                    data_transformed = cls._transform_dict_data(dict_data_list)
                logger.info(f'Total transformed items {len(data_transformed)}')

                cls.data.append((resource.year, [*cls._unify_district_neighborhood_data(data_transformed)]))
                logger.info(f'Total unified items {len(cls.data)}')

            duration = time.time() - start_time
        print(f"Process time: {duration} seconds")

    @classmethod
    def get_average_occupancy(cls) -> tuple:
        if not hasattr(cls, 'data'):
            raise Exception("Method initialize_data() not called. Class needs initialization")

        return DataService.normalize_data(
            cls.data,
            category_attr=lambda item: f'{getattr(item, "name_district")} / {getattr(item, "name_neighborhood")}',
            value_attr=lambda item: getattr(item, "average_occupancy"))

    @staticmethod
    def _transform_dict_data(dict_data_list: list) -> list:
        data = []
        for dict_data in dict_data_list:
            data.append(AverageTouristOccupancyService._create_object(dict_data))
        return data

    @staticmethod
    def _create_object(dict_data: dict):
        try:
            average_tourist_occupancy_price = AverageTouristOccupacy(
                dict_data[AVG_TOURIST_OCCUPANCY.DISTRICT_NAME],
                dict_data[AVG_TOURIST_OCCUPANCY.NEIGHBORHOOD_NAME],
                dict_data[AVG_TOURIST_OCCUPANCY.ACCOMMODATION_TYPE],
                dict_data[AVG_TOURIST_OCCUPANCY.PRICE],
                dict_data[AVG_TOURIST_OCCUPANCY.AVAILABILITY]
            )
            return average_tourist_occupancy_price
        except Exception as e:
            logger.error(f'An error reading transform data', exc_info=True, extra={'exception': e})

    @staticmethod
    def _unify_district_neighborhood_data(data: list) -> list:
        """
        Unify year quarter data
        :param data:
        :return:
        """
        # group all data by same district and neighborhood
        temp_data_dict = dict()
        for item in data:
            key = f'{item.name_district}${item.name_neighborhood}'
            if key in temp_data_dict:
                dict_items = temp_data_dict[key]
                dict_items.append(item)
            else:
                temp_data_dict[key] = [item]

        # calculate the average occupancy of each grouped list
        for key, values in temp_data_dict.items():
            average_occupancy = AverageTouristOccupacy(
                values[0].name_district,
                values[0].name_neighborhood
            )
            average_occupancy.average_occupancy = len(values)
            temp_data_dict[key] = average_occupancy

        return temp_data_dict.values()


class DataService:

    @staticmethod
    def fetch_data(url: str, offset: int) -> list:
        data_list = []

        # first call to know total amount of data
        urls = [{'url': url, 'params': {}}]
        data = asyncio.run(fetch_all_data(urls))

        if data:
            data_list.extend(data)
            json_data = data[0]
            if json_data and json_data['success'] is True:
                total_records = json_data['result']['total']
                logger.info(f'Total records to fetch {total_records}')
                requests = total_records // offset

                # fetch data with offset
                endpoints = []
                for i in range(1, requests + 1):
                    endpoint = {
                        'url': url,
                        'params': {
                            'offset': f'{i * offset}'
                        }
                    }
                    endpoints.append(endpoint)
                data_list.extend(asyncio.run(fetch_all_data(endpoints)))
        return data_list

    @staticmethod
    def read_data(csv_file: str) -> list:
        data_list = []
        with open(csv_file.path, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data_list.append(row)
        return data_list

    @staticmethod
    def normalize_data(data_list: list, category_attr: Callable, value_attr: Callable) -> tuple:
        categories = set()
        normalized_data_list = []
        tmp_data_list = []

        for year, data in data_list:
            values = data if data else []

            tmp_data = []
            for value in values:
                category = category_attr(value)
                categories.add(category)
                data_dict = {
                    'category': category,
                    'value': value_attr(value)
                }
                tmp_data.append(data_dict)
            tmp_data_list.append((year, tmp_data))

        # all year data need to have same categories, fill without value
        for year, tmp_list in tmp_data_list:
            tmp_categories = set()
            for tmp_data_dict in tmp_list:
                tmp_categories.add(tmp_data_dict['category'])

            # check difference between categories and add the different without value
            diffs = categories.difference(tmp_categories)
            logger.info(f"Differences: {diffs}")
            for diff in diffs:
                tmp_list.append({
                    'category': diff,
                    'value': 0
                })
            # sort elements by category key
            tmp_list = sorted(tmp_list, key=itemgetter('category'))
            # get only values
            tmp_values = []
            for tmp_item in tmp_list:
                tmp_values.append(tmp_item['value'])

            normalized_data_list.append({'year': year, 'values': tmp_values})

        # finally sort categories
        categories = sorted(categories)

        return categories, normalized_data_list
