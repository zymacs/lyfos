from django.contrib import admin
from .models import Record, Product, Brand, Vendor, Flavor, FoodProductVariant, Branch

# Register your models here.
admin.site.register(Product)
admin.site.register(Record)
admin.site.register(Brand)
admin.site.register(Vendor)
admin.site.register(Flavor)
admin.site.register(FoodProductVariant)
admin.site.register(Branch)
