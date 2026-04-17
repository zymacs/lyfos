from django.db import models
from movements.models import MovementLog
from places.models import Address


# Create your models here.
ProductUnits = [
    ('ml', 'millilitre'),
    ('L','Litre'),
    ('g', 'gram'),
    ('kg','kilogram'),
    ('m', 'months'),
    ('loaf', 'Loaf'),
    ('u', 'Unit'),
    ('t','Trip'),
]


PackagingChoices = [
    ('sachet', 'Sachet'),
    ('bottle', 'Bottle'),
    ('packet', 'packet'),
    ('can','Can'),
    ('tin', 'Tin'),
    ('polythene', 'Polyethene'),
    ('paperbag','Paperbag'),
    ('box','Box'),
]

PackagingMaterial = [
    ('plastic','Plastic'),
    ('polyethene', 'Polyethene'),
    ('aluminium', 'Aluminium'),
    ('paper','Paper'),
]



class Brand(models.Model):
    name = models.CharField(max_length=1024)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name

class Vendor(models.Model):
    name = models.CharField(max_length=1024)
    def __str__(self):
        return self.name

# business specific place modeling
class Branch(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='branches')
    name = models.CharField(max_length=255, default='None') # Main Office, Downtown Branch
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'branches'
    
    def __str__(self):
        return f"{str(self.vendor)} {str(self.name)}"


class FoodProductVariant(models.Model):
    """
    powdered, seed, sliced, etc
    """
    variant = models.CharField(max_length=1024)

    def __str__(self):
        return self.variant


    
class Product(models.Model):
    product_name = models.CharField(max_length=1024)
    product_type = models.CharField(choices=[('liquid','Liquid'),('solid','Solid'),('service','Service'),('powder','Powder'),('physica','Physical')])
    product_units = models.CharField(choices=ProductUnits, max_length=1000, null=True, blank=True)

    class Meta:
        ordering = ["-product_name"]

    def __str__(self):
        return self.product_name

class Flavor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


    
    
class Record(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_log = models.ForeignKey(MovementLog, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    flavor = models.ForeignKey(Flavor, on_delete=models.SET_NULL, null=True, blank=True)
    food_product_variant = models.ForeignKey(FoodProductVariant, null=True, blank=True, on_delete=models.SET_NULL)
    packaging = models.CharField(choices=PackagingChoices, default='sachet', null=True, blank=True)
    packaging_material = models.CharField(choices=PackagingMaterial, default='plastic', null=True, blank=True)
    transaction_date = models.DateField()
    record_units = models.CharField(choices=ProductUnits, )
    qty_bought = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.CASCADE)
    record_notes =  models.TextField(null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["-transaction_date"]


    def __str__(self):
        return f'{self.transaction_date}   | {self.product} | {self.brand if self.brand else "NoBrand"}  |  {self.total_price}'
