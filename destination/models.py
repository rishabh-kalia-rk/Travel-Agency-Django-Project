from django.db import models

# Create your models here.
from django.conf import settings

class Destination(models.Model):
    status=[('Open','Open'),('Close','Close')]
    place_name=models.CharField(max_length=30)
    place_picture=models.ImageField(null=True, blank=True,upload_to="profile_pictures/")
    place_description = models.TextField(max_length=200)
    place_status=models.CharField(max_length=10,choices=status,default="Open")

    def __str__(self):
        return f"{self.place_name}"
    
   