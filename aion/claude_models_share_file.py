# model 1: finance app
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

    def __str__(self):
        return self.name

class Vendor(models.Model):
    name = models.CharField(max_length=1024)
    def __str__(self):
        return self.name

class Branch(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, related_name='branches')
    name = models.CharField(max_length=255) # Main Office, Downtown Branch
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name




class FoodProductVariant(models.Model):
    """
    powdered, seed, sliced, etc
    """
    variant = models.CharField(max_length=1024)


    
class Product(models.Model):
    product_name = models.CharField(max_length=1024)
    product_type = models.CharField(choices=[('liquid','Liquid'),('solid','Solid'),('service','Service'),('powder','Powder')])
    product_units = models.CharField(choices=ProductUnits, max_length=1000, null=True, blank=True)

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
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f'{self.transaction_date}   | {self.product} | {self.brand if self.brand else "NoBrand"}  |  {self.total_price}'

# -- ends here ---

# model 2: contacts app

from django.db import models
from entity.models import Entity


SOCIAL_PLATFORMS = [
    ('facebook','Facebook'),
    ('instagram','Instagram'),
    ('telegram','Telegram'),
    ('youtube','YouTube'),
]


TELECOM_PROVIDERS = [
    ('mtn','MTN'),
    ('airtel','Airtel'),
    ('kktcell','KKTCELL')
]



class PhoneNumber(models.Model):
    entity =  models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="phone_numbers", blank=True, null=True)
    provider = models.CharField(max_length=100, choices=TELECOM_PROVIDERS, blank=True, null=True)
    number = models.CharField(max_length=15)
    country_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.country_code}-{self.number}"


class Email(models.Model):
    entity =  models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="emails", blank=True, null=True)
    email = models.CharField(max_length=100)
    # add email validation logic

    def __str__(self):
        return self.email

class SocialMediaHandle(models.Model):
    entity =  models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="social_media_handles", blank=True, null=True)
    handle = models.CharField(max_length=200)
    platform = models.CharField(choices=SOCIAL_PLATFORMS, default='facebook')


    def __str__(self):
        return f"{self.platform.title()} | {self.handle}"
# Create your models here.


    
# --- ends here ---

# model3: aion_calendar

from django.db import models
from datetime import datetime, timedelta
from dateutil import rrule


# Create your models here.

class CalendarSystem(models.Model):

    name = models.CharField(max_length=100)
    timezone = models.CharField(max_length=50, default='Asia/Famagusta')

    weekend_days = models.JSONField(default=[5,6])
    business_hours_start = models.TimeField(null=True, blank=True)
    business_hours_end = models.TimeField(null=True, blank=True)

    def is_business_day(self, date):
        if date.weekday() in self.weekend_days:
            return False
        return True
    
    #TODO: implement skip for holidays

    def get_next_business_day(self, date):
        """Get next business day. Skip weekends/holidays"""
        next_date = date + timedelta(days=1)
        while not self.is_business_day(next_date):
            next_date += timedelta(days=1)
        return next_date


class MissingDatePolicy(models.TextChoices):
    SKIP = 'skip', "Skip months without this date."
    LAST_DAY = 'last_day', "Use last day of month."
    NEXT_DAY = 'next_day', "Use next day that exists."
    PREV_DAY = 'prev_day', "Use previous day that exists."
    ADJUST_TO = 'adjust_to', "Adjust to specific day."

    

class SchedulePattern(models.Model):

    name = models.CharField(max_length=100)
    missing_date_policy = models.CharField(
        max_length=20,
        choices=MissingDatePolicy.choices,
        default=MissingDatePolicy.LAST_DAY,
        help_text="What to do when the requested date doesn't exist."
    )

    # FOR ADJUST_TO POLICY
    fallback_day = models.IntegerField(
        null=True,
        blank=True,
        help_text="Day of month to use when original doesn't exist"
    )
    
    freq = models.CharField(max_length=20, choices=[
        ('YEARLY','yearly'),
        ('MONTHLY', 'monthly'),
        ('WEEKLY', 'weekly'),
        ('DAILY','daily'),
        ('HOURLY','hourly'),
    ])
    interval = models.IntegerField(default=1)
    byweekday = models.JSONField(null=True, blank=True)
    bymonthday = models.JSONField(null=True, blank=True) # 1, 15, 28, 30
    bymonth = models.JSONField(null=True, blank=True) # 1,4,7,10 for quarterly
    bysetpos = models.IntegerField(null=True, blank=True)

    until = models.DateTimeField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)

    week_start = models.IntegerField(default=6) # Sunday

    def to_rrule(self, dtstart):
        params = {
            'freq': getattr(rrule, self.freq),
            'interval': self.interval,
            'dtstart': dtstart
        }

        if self.byweekday:
            params['byweekday'] = [getattr(rrule, d.upper()) for d in self.byweekday]
        if self.bymonthday:
            params['bymonthday'] = self.bymonthday
        if self.bymonth:
            params['bymonth'] = self.bymonth
        if self.bysetpos:
            params['bysetpos'] = self.bysetpos
        if self.until:
            params['until'] = self.until
        if self.count:
            params['count'] = self.count

        return rrule(**params)
    
class Schedule(models.Model):

    name = models.CharField(max_length=100)
    pattern = models.ForeignKey(SchedulePattern, on_delete=models.CASCADE)
    calendar = models.ForeignKey(CalendarSystem, on_delete=models.CASCADE)

    effective_start = models.DateTimeField()
    effective_end = models.DateTimeField(null=True, blank=True)

    apply_business_days_only = models.BooleanField(default=False)
    apply_business_hours_only = models.BooleanField(default=False)
    roll_to_business_day = models.BooleanField(default=False)

    overrides = models.JSONField(default=dict, blank=True)

    def get_occurences(self, start_date, end_date):
        occurences =  []

        rule = self.pattern.to_rrule(start_date)
        candidates = rule.between(start_date, end_date, inc=True)

        for candidate in candidates:

            if self.apply_business_days_only:
                if not self.calendar.is_business_day(candidate):
                    if self.roll_to_business_day:
                        candidate = self.calendar.get_next_business_day(candidate)
                    else:
                        continue
                    
            if self.apply_business_hours_only and self.calendar.business_hours_start:
                candidate = candidate.replace(
                    hour=self.calendar.business_hours_start.hour,
                    minute=self.calendar.business_hours_start.minute
                )

            occurrences.append(candidate)

        return occurences


# -- ends here ---
# -- model4: person

import uuid

from django.db import models

from entity.models import Entity, EntityType

from django.contrib.contenttypes.models import ContentType

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation



# Create your models here.

class Person(models.Model):
   
    #entity = models.OneToOneField(Entity, on_delete=models.CASCADE, primary_key=True, related_name='person_detail')
    firstname = models.CharField(max_length=1024)
    lastname = models.CharField(max_length=1024)
    nicknames = models.CharField(max_length=1024, blank=True, null=True)
    # entity_id = uuid.uuid4()
    gender = models.CharField(choices=[('male','Male'),('female','Female')], max_length=6, blank=True, null=True)
    entity_type = models.ForeignKey(EntityType, on_delete=models.CASCADE, null=True, blank=True)
    
    # bio
    dob = models.DateField(blank=True, null=True)


    entities = GenericRelation(
        'entity.Entity',
        content_type_field = 'content_type',
        object_id_field = 'object_id',
        related_query_name = 'person'
    )
    
    def save(self, *args, **kwargs):
        #if not self.entity_id:
        #    self.entity_id = uuid.uuid4()
        
        # create an entity entry for person
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            
            self.entities.create(
                entity_type=self.entity_type
            )
           
    def __str__(self):
        return f"{self.firstname} {self.lastname}".title() 


class RelationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    reverse_name = models.CharField(max_length=100, blank=True, null=True, help_text="One-way relation if empty.")
    biological =  models.BooleanField(default=False)
    category = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return self.name

class Relation(models.Model):

    from_entity = models.ForeignKey(Entity, related_name="outgoing", on_delete=models.CASCADE)
    to_entity = models.ForeignKey(Entity, related_name="incoming", on_delete=models.CASCADE)
    relation_type = models.ForeignKey(RelationType, on_delete=models.CASCADE)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    is_bidirectional = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['from_entity', 'to_entity', 'relation_type']
        indexes = [
            models.Index(fields=['from_entity']),
            models.Index(fields=['to_entity']),
            ]
        
    @classmethod
    def get_bidirectional(cls, entity_1, entity_2, relation_type):
        """Get relation regardless of direction for symmetric types"""
        if not relation_type.is_bidirectional:
            return cls.objects.filter(
                from_entity=entity_1,
                to_entity=entity_2,
                relation_type=relation_type
            ).first()
        
        # For bidirectional, check both directions
        return cls.objects.filter(
            models.Q(from_entity=entity_1, to_entity=entity_2) |
            models.Q(from_entity=entity_2, to_entity=entity_1),
            relation_type=relation_type
        ).first()    


    

    def __str__(self):
        return f"{self.from_entity} → {self.relation_type} → {self.to_entity}"

