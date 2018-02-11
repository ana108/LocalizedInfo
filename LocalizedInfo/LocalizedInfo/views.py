from django.http import HttpResponse
from django.template import loader
from services.UserLocation import UserLocation, LocationWeather, LocalNews
import json

def ipAddr(request):
    geo = UserLocation(request.GET['address'])
    locBasics = geo.geoLocate()
    weather = LocationWeather(locBasics['longitude'], locBasics['latitude'])
    jsonWeather = weather.getWeather()
    response = {}
    response['locInfo'] = locBasics
    response['weatherInfo'] = jsonWeather
    localNews = LocalNews(locBasics['city'], locBasics['country'])
    localNews.getTopTen()
    return HttpResponse(json.dumps(response))

def index(request):
    template = loader.get_template('LocalizedInfo/index.html')
    context = {
        'ipLabel': 'Enter an IPV4 address',
    }
    return HttpResponse(template.render(context, request))

