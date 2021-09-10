from django.db import models
from django.db.models.fields.related import ForeignKey


class Address(models.Model):
    nb = models.CharField(max_length=10)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    zip = models.IntegerField()

    def __str__(self) -> str:
        return '%s %s, %s, %s'%(self.street , self.nb , self.city, self.zip)


class Firms(models.Model):
    name = models.CharField(max_length=50)
    CHE = models.CharField(max_length=15)
    date = models.CharField(max_length=10)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    canton = models.CharField(max_length=10)
    admin = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name
    

    
class TestDb(models.Model):
    name=models.CharField(max_length=10)
    oui = models.CharField(max_length=10)