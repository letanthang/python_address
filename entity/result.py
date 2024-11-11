class Result:
    def __init__(self, ward='', district='', province=''):
        self.ward = ward
        self.district = district
        self.province = province

    def is_complete(self):
        return all([self.ward, self.district, self.province])