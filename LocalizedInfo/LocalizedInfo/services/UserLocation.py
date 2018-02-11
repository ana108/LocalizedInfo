from .. import models 
from django.contrib.gis.geoip2 import GeoIP2
import os

class UserLocation():
    

    def __init__(self, ipAddress):
        self.ipAddress = ipAddress
        
    #def checkIfExists(self):
        #addr = models.Location(self.ipAddress);
        #Todo figure out how to retrieve from db
        #if none found, call service api.
        
    def geoLocate(self):
        g = GeoIP2()
        print g.city(self.ipAddress)
        print g.city(self.ipAddress)['city']
        print g.country(self.ipAddress)['country_name']
        print g.lat_lon(self.ipAddress)[0] #latitude
        print g.lat_lon(self.ipAddress)[1]
        locValues = {}
        locValues['city'] = g.city(self.ipAddress)['city']
        locValues['postalCode'] = g.city(self.ipAddress)['postal_code']
        locValues['country'] = g.country(self.ipAddress)['country_name']
        locValues['latitude'] = g.lat_lon(self.ipAddress)[0]
        locValues['longitude'] = g.lat_lon(self.ipAddress)[1]
        
        return locValues
    
class LocationWeather():
    
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude