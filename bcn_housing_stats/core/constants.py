from enum import Enum
from types import SimpleNamespace

AVG_RENTAL_PRICE_KEY = {
    'ID': "_id",
    'CONCEPT': "Lloguer_mitja",
    'DISTRICT_CODE': "Codi_Districte",
    'DISTRICT_NAME': "Nom_Districte",
    'NEIGHBORHOOD_CODE': "Codi_Barri",
    'NEIGHBORHOOD_NAME': "Nom_Barri",
    'QUARTER': "Trimestre",
    'PRICE': "Preu",
    'YEAR': "Any"
}
AVG_RENTAL_PRICE_KEY = SimpleNamespace(**AVG_RENTAL_PRICE_KEY)

AVG_RENTAL_PRICE_VALUE_CONCEPT_MONTHLY_RENTAL = "Lloguer mitjà mensual (Euros/mes)"
AVG_RENTAL_PRICE_VALUE_PRICE_NA = "NA"
