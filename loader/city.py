#class CityPeriod:
#    def __init__(self):


class City:
    def __init__(self, id, latitude, longitude, elevation):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

    def id(self):
        return self.id
