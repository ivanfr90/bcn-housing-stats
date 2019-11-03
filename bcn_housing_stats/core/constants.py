from enum import Enum
from types import SimpleNamespace

AVG_RENTAL_PRICE = {
    "ID": "_id",
    "CONCEPT": "Lloguer_mitja",
    "DISTRICT_CODE": "Codi_Districte",
    "DISTRICT_NAME": "Nom_Districte",
    "NEIGHBORHOOD_CODE": "Codi_Barri",
    "NEIGHBORHOOD_NAME": "Nom_Barri",
    "QUARTER": "Trimestre",
    "PRICE": "Preu",
    "YEAR": "Any"
}
AVG_RENTAL_PRICE = SimpleNamespace(**AVG_RENTAL_PRICE)

AVG_RENTAL_PRICE_VALUE_CONCEPT_MONTHLY_RENTAL = "Lloguer mitjà mensual (Euros/mes)"
AVG_RENTAL_PRICE_VALUE_PRICE_NA = "NA"


AVG_OCCUPANCY = {
    "ID": "_id",
    "DISTRICT_CODE": "Codi_Districte",
    "DISTRICT_NAME": "Nom_Districte",
    "NEIGHBORHOOD_CODE": "Codi_Barri",
    "NEIGHBORHOOD_NAME": "Nom_Barri",
    "HOUSES": "Domicilis",
    "POPULATION": "Poblacio",
    "AVERAGE_OCCUPANCY": "Ocupacio_mitjana_(persones_ per_domicili)",
    "YEAR": "Any"
}
AVG_OCCUPANCY = SimpleNamespace(**AVG_OCCUPANCY)


AVG_TOURIST_OCCUPANCY = {
    "ID": "id",
    "DISTRICT_NAME": "neighbourhood_group",
    "NEIGHBORHOOD_NAME": "neighbourhood",
    "ACCOMMODATION_TYPE": "room_type",
    "PRICE": "price",
    "AVAILABILITY": "availability_365"
}
AVG_TOURIST_OCCUPANCY_ACCOMMODATION_TYPE_FULL = "Entire home/apt"
AVG_TOURIST_OCCUPANCY_ACCOMMODATION_TYPE_PART = "Private room"
AVG_TOURIST_OCCUPANCY = SimpleNamespace(**AVG_TOURIST_OCCUPANCY)
