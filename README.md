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
	
Step 3. - Set up the following environment variables:
	OPEN_WEATHER_API - see value in email
	EVENT_REGISTRY_API - see value in email
	
Step 5. - Run the following python commands.
	navigate to Project/LocalizedInfo/LocalizedInfo, such that you are in the same directory as manage.python
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver

Step 6. Navigate to localhost:8000 to view the page. Enter a valid ip4 or ip6 address to test.