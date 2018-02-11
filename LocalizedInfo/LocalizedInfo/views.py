from django.http import HttpResponse
from django.template import loader
from services.UserLocation import UserLocation
import json

def ipAddr(request):
    print 'Received request'
    print request.GET['address']
    ul = UserLocation(request.GET['address'])
    locBasics = ul.geoLocate()
    response = json.dumps(locBasics)
    return HttpResponse(response)

def index(request):
    print 'Hello World'
    template = loader.get_template('LocalizedInfo/index.html')
    context = {
        'ipLabel': 'Enter an IPV4 address',
    }
    return HttpResponse(template.render(context, request))

