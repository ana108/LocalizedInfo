from django.db import models

class Location(models.Model):
    #author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    ipAddress = models.TextField()
    city = models.TextField()
    countryCode = models.CharField(max_length=50);
    postalCode = models.CharField(max_length=15);
    latitude = models.DecimalField(max_digits=10,decimal_places=2);
    longitude = models.DecimalField(max_digits=10,decimal_places=2);

    def publish(self):
        #Do not write if is already in db
        self.save()

    def __str__(self):
        return self.ipAddress