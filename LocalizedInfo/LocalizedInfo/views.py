from django.http import HttpResponse
from django.conf import settings
from django.template import loader
from .UserLocation import UserLocation, LocationWeather, LocalNews
import json
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def ipAddr(request):
    geo = UserLocation(request.GET['address'])
    locBasics = geo.geoLocate()[1]
    weather = LocationWeather(locBasics['longitude'], locBasics['latitude'])
    jsonWeather = weather.getWeather()
    response = {}
    response['locInfo'] = locBasics
    response['weatherInfo'] = jsonWeather
    localNews = LocalNews(locBasics['city'], locBasics['country'])
    news = localNews.getTopTen()
    if news[0] == 0:
        response['news'] = news[1]
    return HttpResponse(json.dumps(response))

def index(request):
    template = loader.get_template('LocalizedInfo/index.html')
    context = {
        'ipLabel': 'Enter an IP address',
    }
    return HttpResponse(template.render(context, request))

