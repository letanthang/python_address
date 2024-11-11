class Ward:
    def __init__(self, name='', no_prefix_name='', code='', province='', province_code='', district='', district_code='', type_=''):
        self.name = name
        self.no_prefix_name = no_prefix_name
        self.code = code
        self.province = province
        self.province_code = province_code
        self.district = district
        self.district_code = district_code
        self.type = type_


class Province:
    def __init__(self, name='', no_prefix_name='', code=''):
        self.name = name
        self.no_prefix_name = no_prefix_name
        self.code = code


class District:
    def __init__(self, name='', no_prefix_name='', code='', province_code=''):
        self.name = name
        self.no_prefix_name = no_prefix_name
        self.code = code
        self.province_code = province_code


class LocationType:
    OTHER = 0
    WARD = 1
    DISTRICT = 2
    PROVINCE = 3

    @staticmethod
    def to_string(location_type):
        if location_type == LocationType.WARD:
            return "Ward"
        elif location_type == LocationType.DISTRICT:
            return "District"
        elif location_type == LocationType.PROVINCE:
            return "Province"
        else:
            return "Other"


class Location:
    def __init__(self, name='', location_type=LocationType.OTHER, location_id='', weight=0):
        self.name = name
        self.location_type = location_type
        self.id = location_id
        self.weight = weight

    def to_string(self):
        return f"{self.name}-{LocationType.to_string(self.location_type)}-{self.id}"


class Locations:
    def __init__(self, locations=None):
        self.locations = locations if locations else []

    def to_string(self):
        return "Locations: " + "|".join(location.to_string() for location in self.locations)

    def simplify(self):
        location_map = {location.id: location for location in self.locations}
        province_ids = [location.id for location in self.locations if location.location_type == LocationType.PROVINCE]
        district_ids = [location.id for location in self.locations if location.location_type == LocationType.DISTRICT]
        ward_ids = [location.id for location in self.locations if location.location_type == LocationType.WARD]
        return location_map, ward_ids, district_ids, province_ids

    def len(self):
        return len(self.locations)

    def sort_by_weight(self):
        self.locations.sort(key=lambda x: x.weight, reverse=True)