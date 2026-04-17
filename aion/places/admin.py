from django.contrib import admin
from .models import Country, City, Area, Address

# Register your models here.

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(Address)
