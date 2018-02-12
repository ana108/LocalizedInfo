from models import Location, Weather, LocalArticle 
from django.contrib.gis.geoip2 import GeoIP2
from eventregistry import EventRegistry, QueryArticlesIter
import os, requests, json, datetime
#from django_redis import cache
from django_redis.cache import RedisCache
from django.core.cache import cache

class UserLocation():    
    
    def __init__(self, ipAddress):
        self.ipAddress = ipAddress
        
        
    def geoLocate(self):
        obj = cache.get(self.ipAddress)
        if obj == None:
            locationData = Location.objects.filter(ipAddress=self.ipAddress)
                 
            if locationData.exists():
                locValues = {}
                locValues['city'] = locationData[0].city
                locValues['postalCode'] = locationData[0].postalCode
                locValues['country'] = locationData[0].country
                locValues['latitude'] = str(locationData[0].latitude)
                locValues['longitude'] = str(locationData[0].longitude)
            else:
                g = GeoIP2()
                locValues = {}
                locValues['city'] = g.city(self.ipAddress)['city']
                locValues['postalCode'] = g.city(self.ipAddress)['postal_code']
                locValues['country'] = g.country(self.ipAddress)['country_name']
                locValues['latitude'] = g.lat_lon(self.ipAddress)[0]
                locValues['longitude'] = g.lat_lon(self.ipAddress)[1]
                location = Location(ipAddress=self.ipAddress, city=locValues['city'], postalCode=locValues['postalCode'], country=locValues['country'],latitude=locValues['latitude'], longitude=locValues['longitude']);
                location.save()
                
            cache.set(self.ipAddress, locValues)
            return 0,locValues
        else:
            return 0, cache.get(self.ipAddress)
        
    
    def setCache(self, ipAddress, locationObj):
        cache.set(ipAddress, locationObj)
        
class LocationWeather():
    
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude
        
    def getWeather(self):
        weatherId = str(datetime.date.today()) + "," + str(self.latitude) + "," + str(self.longitude);
        weatherCache = cache.get(weatherId)
        if weatherCache == None:
            if Weather.objects.filter(latitude=self.latitude, longitude=self.longitude,date=datetime.date.today()).exists():
                weather = Weather.objects.get(latitude=self.latitude, longitude=self.longitude,date=datetime.date.today())
                weatherDict = {}
                weatherDict['status'] = weather.description
                weatherDict['Temperature'] = str(weather.temperature)
                return weatherDict
            else:    
                apikey = "&APPID=" + os.environ['OPEN_WEATHER_API']
                if os.environ['OPEN_WEATHER_API'] == None:
                    raise
                
                cityIdUrl = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(self.latitude) + "&units=metric&lon=" + str(self.longitude) +apikey
                
                response = requests.get(cityIdUrl)
                if response.status_code == 200:
                    rawContent = json.loads(response.content)
                    weatherDict = {}
                    weatherDict['status'] = rawContent['weather'][0]['description']
                    weatherDict['Temperature'] = rawContent['main']['temp']
                    weather = Weather(latitude=self.latitude, longitude=self.longitude,date=datetime.date.today(),description=weatherDict['status'],temperature=weatherDict['Temperature'])
                    weather.save()
                    cache.add(weatherId, weatherDict)
                    return weatherDict
                else: 
                    return "No weather could be found for these coordinates"
        else:
            return weatherCache
        
class LocalNews():
    def __init__(self, city, country=None):
        self.city = city
        if self.city == None:
            self.city = ""
        self.country = country
    
    def getTopTen(self):
        articleCache = cache.get(str(datetime.date.today()) + "," + self.city + " " + self.country)
        if articleCache == None:
            articles = LocalArticle.objects.filter(city=self.city,country=self.country,date=datetime.date.today())
            if articles.exists():
                articlesToSend = []
                for article in articles:
                    articleDict = {}
                    articleDict['title'] = article.title
                    articleDict['url'] = article.url
                    articlesToSend.append(articleDict)
                
                return 0, articlesToSend;
            
            startDate = datetime.date.today() - datetime.timedelta(days=1)
            try:
                eventRegistryApi = os.environ['EVENT_REGISTRY_API']
            except:
                return -1,'Could not find event registry api key'
            
            er = EventRegistry(apiKey = eventRegistryApi, repeatFailedRequestCount=1)
            q = QueryArticlesIter(dateStart = startDate, locationUri = [er.getLocationUri(self.city),er.getLocationUri(self.country)], sourceLocationUri=er.getLocationUri(self.country)) #
            
            res = q.execQuery(er, maxItems=10)
            it = iter(res)
            arrOfArticles = []
            for article in it:
                if article['isDuplicate'] == False:
                    dbArticle = LocalArticle(city=self.city, country=self.country, date=datetime.date.today(), title=article['title'],url=article['url'])
                    dbArticle.save()
                    articleDict = {}
                    articleDict['title'] = article['title']
                    articleDict['url'] = article['url']
                    arrOfArticles.append(articleDict)
            
            return 0,arrOfArticles #success, info, otherwise, fail
        else:
            return articleCache
        