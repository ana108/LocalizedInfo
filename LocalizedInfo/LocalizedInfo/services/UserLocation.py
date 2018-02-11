from .. import models 
from django.contrib.gis.geoip2 import GeoIP2
from eventregistry import *
import os, requests, json

class UserLocation():
    

    def __init__(self, ipAddress):
        self.ipAddress = ipAddress
        
    #def checkIfExists(self):
        #addr = models.Location(self.ipAddress);
        #Todo figure out how to retrieve from db
        #if none found, call service api.
        
    def geoLocate(self):
        g = GeoIP2()
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
        
    def getWeather(self):
        apikey = "?apikey=" + os.environ['ACCUWEATER_API']
        cityIdUrl = "https://dataservice.accuweather.com/locations/v1/cities/geoposition/search"+apikey
        coordinates = "&q=" + str(self.latitude) + "," + str(self.longitude)
        cityIdUrl += coordinates
        
        response = requests.get(cityIdUrl)
        if response.status_code == 200:
            cityId = json.loads(response.content)['Key']
            weatherStatusUrl = "https://dataservice.accuweather.com/currentconditions/v1/" + cityId + apikey
            response = requests.get(weatherStatusUrl)
            if response.status_code == 200:
                rawContent = json.loads(response.content)
                weatherDict = {};
                weatherDict['status'] = rawContent[0]['WeatherText']
                weatherDict['Temperature'] = rawContent[0]['Temperature']['Metric']['Value']
                return weatherDict
            else:
                return "No weather information could be retrieved. " #TODO store the city name
        else: 
            return "No city could be found for these coordinates"
        
class LocalNews():
    def __init__(self, city, country=None):
        self.city = city
        self.country = country
    
    def getTopTen(self):
        er = EventRegistry(apiKey = '5526932d-7dc0-462f-806d-a7251cd4d9fb')
        q = QueryArticlesIter(dateStart = datetime.date(2018, 2, 10),locationUri = er.getLocationUri(self.city))
        res = er.execQuery(q)
        arrOfArticles = res['articles']['results']
        for i in range(0, len(arrOfArticles)):
            print arrOfArticles[i]['title']
            print arrOfArticles[i]['url']
        