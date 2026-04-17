from django.db import models

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)

    
    class Meta:
        verbose_name_plural = 'countries'


    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'cities'
        
    def __str__(self):
        return f"{self.name} |  {self.country}"

class Area(models.Model):
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Address(models.Model):
    area = models.ForeignKey(Area, on_delete=models.PROTECT, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    street = models.CharField(max_length=255, blank=True)
    building = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    
    class Meta:
        verbose_name_plural = 'addresses'


    def __str__(self):
        return f"{str(self.area)} {str(self.city)}"

