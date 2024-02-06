
from django.db import models

# Create your models here.

class ValuedItems(models.Model):
    valItems= models.CharField(max_length=255)
    IDitems = models.CharField(max_length=1000)
    
class Participant(models.Model):
    firstName= models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    IDparticipant = models.CharField(max_length=1000)
    item = models.CharField(max_length=255, null=True)
    pay = models.FloatField(blank=True, null=True)
    get = models.FloatField(blank=True, null=True)
    item_id = models.CharField(max_length=1000, blank=True, null=True)

class Bidding(models.Model):
    IDparticipant = models.CharField(max_length=1000)
    total = models.FloatField()
    item1 = models.IntegerField(default = 0)
    item2 = models.IntegerField(default = 0)
    item3 = models.IntegerField(default = 0)
    item4 = models.IntegerField(default = 0)
    item5 = models.IntegerField(default = 0)
    item6 = models.IntegerField(default = 0)
    item7 = models.IntegerField(default = 0)
    item8 = models.IntegerField(default = 0)
    item9 = models.IntegerField(default = 0)
    item10 = models.IntegerField(default = 0)  

class ResultAuction(models.Model):
    firstName= models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    IDparticipant = models.CharField(max_length=1000)
    item = models.CharField(max_length=1000)
    total_value = models.FloatField(default=0)
    fair_share = models.FloatField(default=0)
    pay = models.FloatField(default=0)
    get = models.FloatField(default=0)
    link = models.CharField(max_length=1000)
    
    
    
    