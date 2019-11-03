import asyncio
import csv
import json
import logging
import time
from operator import itemgetter

from bcn_housing_stats.utils.utils import fetch_all_data
from config.settings.base import ResourceTypeSLUGS
from .constants import (
    AVG_RENTAL_PRICE_VALUE_CONCEPT_MONTHLY_RENTAL,
    AVG_RENTAL_PRICE_KEY,
    AVG_RENTAL_PRICE_VALUE_PRICE_NA
)
from .models import Resource

logger = logging.getLogger(__name__)


class AverageRentalPrice():

    def __init__(self,
                 id: int,
                 concept: str,
                 code_district: int,
                 name_district: str,
                 code_neighborhood: int,
                 name_neighborhood: str,
                 quarter: int,
                 price: float,
                 year: int):
        self.id = id
        self.concept = concept
        self.code_district = int(code_district)
        self.name_district = name_district
        self.code_neighborhood = int(code_neighborhood)
        self.name_neighborhood = name_neighborhood
        self.quarter = int(quarter)
        self.price = float(price)
        self.year = int(year)


class AverageRentalPriceService:

    def __init__(self, year: int = None, offset: int = 100):
        self.data = []
        self.year = year
        if not self.year:
            resource = Resource.objects.filter(
                type__slug=ResourceTypeSLUGS.AVERAGE_MONTHLY_RENT.value).order_by('-year').first()
            self.year = resource.year
        else:
            resource = Resource.objects.filter(
                type__slug=ResourceTypeSLUGS.AVERAGE_MONTHLY_RENT.value, year=self.year).first()

        start_time = time.time()
        if resource:
            offset = offset
            url = resource.url
            csv = resource.file

            averages_rental_prices_transformed = []

            # first try from endpoint
            json_data_list = self._fetch_data(url, offset)

            # if fails, try from csv file
            if json_data_list:
                for json_data in json_data_list:
                    averages_rental_prices_transformed += self._transform_json_data(json_data)
            else:
                dict_data_list = self._read_data(csv)
                averages_rental_prices_transformed = self._transform_dict_data(dict_data_list)

            logger.info(f'Total transformed items {len(averages_rental_prices_transformed)}')

            self.data = [*self._unify_year_quarter_data(averages_rental_prices_transformed)]
            logger.info(f'Total unified items {len(self.data)}')

        duration = time.time() - start_time
        print(f"Process time: {duration} seconds")

    @classmethod
    def get_average_rental(cls, year: int = None, offset: int = 100) -> list:
        instance = cls(year, offset)
        data = instance.data
        year = instance.year

        average_rental_values = data if data else []
        categories = set()
        data_list = []

        tmp_data_list = []
        for average_rental_value in average_rental_values:
            data = {
                'category': f'{average_rental_value.name_district} / {average_rental_value.name_neighborhood}',
                'value': average_rental_value.price
            }
            tmp_data_list.append(data)

        # sort elements by category key
        tmp_data_list = sorted(tmp_data_list, key=itemgetter('category'))
        # get only values
        values = []
        for tmp_data_item in tmp_data_list:
            categories.add(tmp_data_item['category'])
            values.append(tmp_data_item['value'])

        data_list.append({'year': year, 'values': values})
        categories = sorted(categories)

        return (categories, data_list)

    @classmethod
    def get_all_average_rentals(cls, years: list, offset: int = 100) -> list:
        categories = set()
        data_list = []
        tmp_data_list = []

        for year_arg in years:
            instance = cls(year_arg, offset)
            data = instance.data
            year = instance.year
            average_rental_values = data if data else []

            tmp_data = []
            for average_rental_value in average_rental_values:
                category = f'{average_rental_value.name_district} / {average_rental_value.name_neighborhood}'
                categories.add(category)
                data = {
                    'category': category,
                    'value': average_rental_value.price
                }
                tmp_data.append(data)
            tmp_data_list.append((year, tmp_data))

        # all year data have to have same categories, fill without value
        for year, tmp_list in tmp_data_list:
            tmp_categories = set()
            for data in tmp_list:
                tmp_categories.add(data['category'])

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

            data_list.append({'year': year, 'values': tmp_values})

        # finally sort categories
        categories = sorted(categories)

        return (categories, data_list)

    @classmethod
    def get_total_average_rental(cls, year: int = None, offset: int = 100) -> float:
        average_rental_values = cls(year, offset).data
        total = 0
        for average_rental_value in average_rental_values:
            total += average_rental_value.price
        avg = total / len(average_rental_values)
        return avg

    @staticmethod
    def _fetch_data(url: str, offset: int) -> list:
        data_list = []

        # first call to know total amount of data
        urls = [{'url': url, 'params': {}}]
        json_data_list = asyncio.run(fetch_all_data(urls))

        if json_data_list:
            json_data = json_data_list[0]
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
                data_list = asyncio.run(fetch_all_data(endpoints))
        return data_list

    @staticmethod
    def _read_data(csv_file: str) -> list:
        data_list = []
        with open(csv_file.path, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data_list.append(row)
        return data_list

    @staticmethod
    def _transform_json_data(json_data: json):
        averages_rental_prices = []
        if json_data and json_data['success'] is True:
            for record in json_data['result']['records']:
                empty_price = record[AVG_RENTAL_PRICE_KEY.PRICE] == AVG_RENTAL_PRICE_VALUE_PRICE_NA
                if not empty_price:
                    averages_rental_prices.append(AverageRentalPriceService._create_object(record))
                else:
                    logger.warning(f'Element {record} with not price')
        return averages_rental_prices

    @staticmethod
    def _transform_dict_data(dict_data_list: list):
        averages_rental_prices = []
        for dict_data in dict_data_list:
            empty_price = dict_data[AVG_RENTAL_PRICE_KEY.PRICE] == AVG_RENTAL_PRICE_VALUE_PRICE_NA
            if not empty_price:
                averages_rental_prices.append(AverageRentalPriceService._create_object(dict_data))
            else:
                logger.warning(f'Element {dict_data} with not price')
        return averages_rental_prices

    @staticmethod
    def _create_object(dict_data: dict):
        try:
            average_rental_price = AverageRentalPrice(
                None,  # CSV files dont have id field
                dict_data[AVG_RENTAL_PRICE_KEY.CONCEPT],
                dict_data[AVG_RENTAL_PRICE_KEY.DISTRICT_CODE],
                dict_data[AVG_RENTAL_PRICE_KEY.DISTRICT_NAME],
                dict_data[AVG_RENTAL_PRICE_KEY.NEIGHBORHOOD_CODE],
                dict_data[AVG_RENTAL_PRICE_KEY.NEIGHBORHOOD_NAME],
                dict_data[AVG_RENTAL_PRICE_KEY.QUARTER],
                dict_data[AVG_RENTAL_PRICE_KEY.PRICE],
                dict_data[AVG_RENTAL_PRICE_KEY.YEAR]
            )
            return average_rental_price
        except Exception as e:
            logger.error(f'An error reading transform data', exc_info=True, extra={'exception': e})

    @staticmethod
    def _unify_year_quarter_data(averages_rental_prices: list):
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
                dict_items = []
                dict_items.append(item)
                averages_rental_prices_dict[key] = dict_items

        # calculate the average monthly rent of each grouped list
        for key, average_rental_price_list in averages_rental_prices_dict.items():
            # average of quarter
            sum = 0
            for average_rental_price in average_rental_price_list:
                sum += average_rental_price.price
            avg = sum / len(average_rental_price_list)

            average_rental_price_list[0].prize = avg
            averages_rental_prices_dict[key] = average_rental_price_list[0]

        return averages_rental_prices_dict.values()
