# LocalizedInfo
Step 1. - Have Redis installed locally
For windows, I used the following url to download: 
	https://github.com/ServiceStack/redis-windows/raw/master/downloads/redis-latest.zip
	
One download, extract the files. 
In command line, nagivate to the newly downloaded directory and use the following command to start the service:
	redis-server.exe redis.windows.conf
	
Ideally, redis would be running on port 6379. If not, settings file will need to be updated in the django project.

Step 2. - Using pip, install the following dependencies:
	pip install django (if necessary)
	pip install eventregistry
	pip install geoip2
	pip install django-redis
	