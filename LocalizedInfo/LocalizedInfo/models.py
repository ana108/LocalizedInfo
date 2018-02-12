from django.db import models

class Location(models.Model):
    #author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    ipAddress = models.TextField(primary_key=True)
    city = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=50)
    postalCode = models.CharField(max_length=15,blank=True, null=True)
    latitude = models.DecimalField(max_digits=10,decimal_places=4)
    longitude = models.DecimalField(max_digits=10,decimal_places=4)
    
    def publish(self):
        #Do not write if is already in db
        self.save()

    def __str__(self):
        return self.ipAddress
    

class Weather(models.Model):
    description = models.TextField()
    temperature = models.DecimalField(max_digits=6, decimal_places=3)
    date = models.DateField()
    latitude = models.DecimalField(max_digits=10,decimal_places=4)
    longitude = models.DecimalField(max_digits=10,decimal_places=4)
    class Meta:
        unique_together = (("latitude", "longitude", "date"))
    def publish(self):
        if not self.objects.filter(latitude=self.latitude, longitude=self.longitude).exists():
            self.save()

    def __str__(self):
        return str(self. date) + "," + str(self.latitude) + "," + str(self.longitude)
    

class LocalArticle(models.Model):
    city = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=50)
    title = models.TextField()
    url = models.TextField()
    date = models.DateField()
    
    def publish(self):
        self.save()

    def __str__(self):
        return str(self. date) + "," + self.city + " " + self.country