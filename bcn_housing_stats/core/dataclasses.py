
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


class AverageResidents:

    def __init__(self,
                 code_district: int,
                 name_district: str,
                 code_neighborhood: str,
                 name_neighborhood: str,
                 houses: str,
                 residents: str,
                 average_occupancy: str,
                 year: str):
        self.code_district = int(code_district)
        self.name_district = name_district
        self.code_neighborhood = int(code_neighborhood)
        self.name_neighborhood = name_neighborhood
        self.houses = int(houses)
        self.residents = int(residents)
        self.average_occupancy = float(average_occupancy)
        self.year = int(year)

class TouristOccupancy:

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

class TouristAccommodationAvg:

    def __init__(self,
                 name_district: str,
                 name_neighborhood: str,
                 total_apartments: int,
                 ):
        self.name_district = name_district
        self.name_neighborhood = name_neighborhood
        self.total_apartments = int(total_apartments)
