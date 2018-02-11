from .. import models 
from django.contrib.gis.geoip2 import GeoIP2
from eventregistry import EventRegistry, QueryArticlesIter
import os, requests, json, datetime
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
        apikey = "&APPID=" + os.environ['OPEN_WEATHER_API']
        if os.environ['OPEN_WEATHER_API'] == None:
            print 'Open Weather Api Key is missing'
            raise
        
        cityIdUrl = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(self.latitude) + "&units=metric&lon=" + str(self.longitude) +apikey
        
        response = requests.get(cityIdUrl)
        if response.status_code == 200:
            rawContent = json.loads(response.content)
            weatherDict = {}
            weatherDict['status'] = rawContent['weather'][0]['description']
            weatherDict['Temperature'] = rawContent['main']['temp']
            return weatherDict
        else: 
            print response
            return "No city could be found for these coordinates"
        
class LocalNews():
    def __init__(self, city, country=None):
        self.city = city
        self.country = country
    
    def getTopTen(self):
        startDate =  datetime.date.today() - datetime.timedelta(days=1)
        try:
            eventRegistryApi = os.environ['EVENT_REGISTRY_API']
        except:
            return -1,'Could not find event registry api key'
        
        er = EventRegistry(apiKey = eventRegistryApi, repeatFailedRequestCount=1)
        q = QueryArticlesIter(dateStart = startDate, locationUri = er.getLocationUri(self.city), sourceLocationUri=er.getLocationUri(self.country))
        
        res = q.execQuery(er, maxItems=10)
        it = iter(res)
        arrOfArticles = []
        for article in it:
            if article['isDuplicate'] == False:
                articleDict = {}
                articleDict['title'] = article['title']
                articleDict['url'] = article['url']
                #article['date']
                #articleDict['body'] = article['body']
                arrOfArticles.append(articleDict)
        
        return 0,arrOfArticles
        