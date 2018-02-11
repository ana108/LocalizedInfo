from ..models import Location, Weather, LocalArticle 
from django.contrib.gis.geoip2 import GeoIP2
from eventregistry import EventRegistry, QueryArticlesIter
import os, requests, json, datetime, redis
class UserLocation():
    

    def __init__(self, ipAddress):
        self.ipAddress = ipAddress
        
        
    def geoLocate(self):
        locationData = Location.objects.filter(ipAddress=self.ipAddress)
        if locationData.exists():
            locValues = {}
            locValues['city'] = locationData.city
            locValues['postalCode'] = locationData.city.postalCode
            locValues['country'] = locationData.country
            locValues['latitude'] = locationData.latitude
            locValues['longitude'] = locationData.longitude
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
            
        return locValues
    def checkCache(self):
        
class LocationWeather():
    
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude
        
    def getWeather(self):
        
        if Weather.objects.filter(latitude=self.latitude, longitude=self.longitude,date=datetime.date.today()).exists():
            weather = Weather.objects.get(latitude=self.latitude, longitude=self.longitude,date=datetime.date.today())
            weatherDict = {}
            weatherDict['status'] = weather.description
            weatherDict['Temperature'] = str(weather.temperature)
            print 'Reusing database data'
            return weatherDict
        else:
            print "Latitude of {}  and longitude of {} on date {} could not be found", str(self.latitude), str(self.longitude), datetime.date.today()
            
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
            weather = Weather(latitude=self.latitude, longitude=self.longitude,date=datetime.date.today(),description=weatherDict['status'],temperature=weatherDict['Temperature'])
            weather.save()
            return weatherDict
        else: 
            print response
            return "No city could be found for these coordinates"
        
class LocalNews():
    def __init__(self, city, country=None):
        self.city = city
        self.country = country
    
    def getTopTen(self):
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
        