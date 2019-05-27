from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from havelorryapp import settings
class Drivers(models.Model):
    address=models.TextField()
    vehicle_number=models.BigIntegerField()
    image=models.FileField(upload_to='static/')
    username=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self):
        return '%s,%s'%(self.username,self.vehicle_number)