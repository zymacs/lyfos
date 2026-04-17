# ./accounts/models.py

from django.db import models

# Create your models here.


"""
creating a vendor now means auto creating an account for the vendor
"""


class Transaction:
    """
    types: transfers, 
    """
    from_account = ''
    to_account = ''
    exchange_rate = ''
    pass

class Account:
    pass

class IncomeAccount:
    pass

class EquityAccount:
    pass

class CheckingAccount:
    pass

class LoanAccount:
    pass

class ExpenseAccount:
    pass

---- ends here ----

# ./aion_calendar/models.py

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

---- ends here ----

# ./contacts/models.py

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

---- ends here ----

# ./entity/models.py

from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

# class Entity(models.Model):
#     """Abstract base - no table"""
#     name = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.name

#     class Meta:
#         abstract = True


# filter content types
# filter their content ids
# use that for choice

class EntityType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Entity(models.Model):
    entity_type = models.ForeignKey(EntityType,on_delete=models.CASCADE, null=True, blank=True)
    
    # Generic foreign key fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey('content_type', 'object_id')

    
    def __str__(self):
        return f"{self.entity_type} -> {self.entity}"

    class Meta:
        verbose_name_plural = 'entities'

---- ends here ----

# ./financial_records/models.py

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

---- ends here ----

# ./goals/models.py

from django.db import models
from django.db.models.functions import Now


from tracker.models import Item, Unit
# from aion_calendar.models import Schedule

# Create your models here.


class Vision(models.Model):
    """
    Where lies the leading stars.
    I want to be a reader. tags: intellectual growth
      - consistent reading habit (enumerable)
      - high reading speed (enumerable)
      - active contributer to a reader's club (can be checked off the box)
      - good at reading out to others  (can be measured through books read out to others)
    I want to be a linux expert. tags: technical
      - learn one new thing daily (enumerable) goal
        - sub goal: get a command for each day
                    code a command from scratch each week (cat in c (simplified), dd in c (simplified) or some how dd works series)
      - create a consistent sharing schedule (enumerable)
        - go to blogger (google's site) and create a linux blog
        - post about your weekly explorations
      - create and share scripts (enumerable)
        - find daily frustrations and create scripts for them
      - build projects around what you learn to help others
        - setup scripts
        - update scripts
      - develop a reading habit
        - even 1 book a year read once every 2 days is a good thing
      - get out of your comfort zone
        - use gentoo
        - do linux from scratch
        - use arch
    I want to own emacs (this will last for ever)
      - one new thing about emacs daily (an emacs command or so)
      - one new lisp trick daily
      - a sheet to keep track of all these commands that you author
    I want to be a quant developer
      - Math and statistics
        - develop a curriculum
        - create a consistent turn up system
        - share knowledge
        - write programs to cement knowlege
        - build projects around written programs and write about the projects
      - CPP proficiency
        - read bjarne's book
      - Algo and ds understanding
        - leet code
        - quant guide book
        - 
      - Networking proficiency
    I want to make my own mobile apps
      - Learn react native
        - 
    I want to understand android
    I want to be etc.
    -- statement
    -- sub statements (description of what that means or what one needs to achieve to be that)

    Want to be healthy
     - water habit
       buy a water bottle
       1 cup daily, 2 cups daily, 1 l daily
     - wake up early habit 
     - sleep early habit
     - mobile usage control habit
     - hygiene habits
     - knowlege about health
       - reading habit
         - cooking, vegeterianism, alt medicines, dangers of sugar etc
       - outputting habit (maybe)

    Want to become better and finances
    - discipline to ascertain where u stand currently
    - logging expenses habit
    - saving habit
    - budgetting habit
    - sticking to the budget habit / discipline
    - reading about finance habit
    
    
    Want to grow spiritually
    - prayer habit
    - turning up for Bible habit
    - topical study completion discipline
    - service habits
      - donation habit
      - greeting habit
      - sharing gospel habit
    """
    name = models.CharField(max_length=1024)



class Progression(models.Model):
    """
    goal: do 5 ... daily for X days
    target: 5
    target_type: min
    progressions_and_durations (pnum:target:duration:success_%age_for_progression): 1:2:X:80, 2:3:X:85, 3:4.5:X:95, 4:5:X:100
    id
    name
    goal
    """
    name = models.CharField(max_length=1024)
    target_type = '' # qty,
    
    
class LevelDependencies:
    """
    id
    dependent level
    dependent on
    dependence criterion
    """
    pass
    

class Level(models.Model):
    """
    (id
    progression id
    tracker habit id
    trial num )
    target type
    start date
    end date
    current avg
    status : (succeeded, active, failed)
    success criteria: (avg for x days, consecutive turn up for x days)
    """
    progression = models.ForeignKey(Progression, null=True, blank=True, on_delete=models.CASCADE)
    habit_tracked = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE)
    trial_num = models.IntegerField(unique=True, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    current_avg = models.FloatField(null=True, blank=True)
    status = models.CharField(choices=[('s','succeeded'),('f','failed'),('a','active'),('u','unstarted'), ('m','maintenance')], default="u")


    def succeeded(self):
        pass
    



class HigherGoal(models.Model):
    higher_goal = models.CharField(max_length=1024)
    def __str__(self):
        return self.higher_goal

class GoalTrial(models.Model):
    # trial1: (goal history) goal_id, trial_number, end_status (success or failure)
    # trial2: (goal history) same goal id, trial_number, 
    pass





class Goal(models.Model):
    goal = models.CharField(max_length=1024, null=True, blank=True)
    name = models.CharField(max_length=1024) # (sleep for 8 hours every day for 5 days)
    progression_number = models.IntegerField(default=1)
    trial_number = models.IntegerField(default=1)
    higher_goal = models.ForeignKey(HigherGoal, on_delete=models.CASCADE, null=True, blank=True)
    goal_item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    goal_item_unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True) # warn
    related_goals = models.ManyToManyField('self', blank=True)
    target_sampling_frequency = models.CharField(choices=[("daily","Daily"),('weekly',"Weekly")], default="daily")
    target_count_per_sample = models.IntegerField(blank=True, null=True) # for quantitative goals
    target_type = models.CharField(choices=[('min','minimum'),('max','maximum'),('exact','exact')], default='min')
    target_time = models.TimeField(null=True, blank=True)
    target_date = models.DateField(null=True, blank=True)
    target_sample_count = models.IntegerField(blank=True, null=True) # how long should the goal last (can be inferred from end date)
    start_date = models.DateField(db_default=Now()) # when does the goal start to be active
    end_date = models.DateTimeField(blank=True, null=True) # deadline

    
    
    def __str__(self):
        return f" {self.name} | {self.higher_goal}"

---- ends here ----

# ./journal/models.py

from django.db import models

# Create your models here.

class Journal(models.Model):
    journal_date = models.DateField()
    journal_time = models.TimeField()
    journal_content = models.TextField()

    def __str__(self):
        return f'{self.journal_date} {self.journal_time}'

---- ends here ----

# ./movements/models.py

from django.db import models

# Create your models here.
class MovementLog(models.Model):
    from_location = models.CharField(max_length=1000)
    to_location = models.CharField(max_length=1000)
    means = models.CharField(choices=[('bus','Bus')], max_length=1000, default='bus')
    movt_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.movt_date}: {self.from_location} --> {self.to_location}"

---- ends here ----

# ./person/models.py

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

---- ends here ----

# ./places/models.py

from django.db import models

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

class Area(models.Model):
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

class Address(models.Model):
    area = models.ForeignKey(Area, on_delete=models.PROTECT, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    street = models.CharField(max_length=255, blank=True)
    building = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

---- ends here ----

# ./progression_manager/models.py

from django.db import models

# Create your models here.

---- ends here ----

# ./promises/models.py

from django.db import models
from goals.models import Goal

# Create your models here.

class Promise(models.Model):

    promise = models.CharField(max_length=1024)
    related_goals = models.ManyToManyField(Goal, blank=True)

    def __str__(self):
        return self.promise

---- ends here ----

# ./tracker/models.py

from django.db import models
from django.db.models.functions import Now
from datetime import timedelta


# Create your models here.

ITEM_TYPES = [
    ("qty","How much of something happens"),
    ("inst","When something happens"),
    ("bool", "If something happens"),
    ("prog", "Going towards some goal"), # say reading a book: tracking start page and end page
]

"""
future plans
- hooks: let user notice when an items data can be derived from other items entries
- prohibit tracking in the future (only track what was done not what will be done)
"""

def to_hrs_mins_secs(time_in_seconds):
    hours = str(time_in_seconds //  3600)
    minutes = str((time_in_seconds % 3600) // 60)
    seconds = str((time_in_seconds % 3600) % 60)

    result = '{hrs} hrs : {mins} mins : {secs} secs'
    result =result.format(hrs=hours, mins=minutes, secs=seconds)
    return result


class Unit(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name
    
    
class Item(models.Model):
    name = models.CharField(max_length=1024)
    record_string = models.CharField(max_length=1024, blank=True, null=True)
    item_type = models.CharField(max_length=1024, choices=ITEM_TYPES)
    unit = models.ForeignKey(Unit, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    tag = models.ManyToManyField(Tag, blank=True)
    hidden  = models.BooleanField(default=False, null=True, blank=True)
    """
    ---- later additions
    target_qty or target_time
    """

    def avg(self):
        pass

    def __str__(self):
        return self.name

    

class Record(models.Model):
    date_recorded = models.DateTimeField(db_default=Now())
    related_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.FloatField(blank=True, null=True)
    action_start_time = models.TimeField(blank=True, null=True)
    action_end_time = models.TimeField(blank=True, null=True)
    start_level =  models.IntegerField(blank=True, null=True)
    end_level =  models.IntegerField(blank=True, null=True)
    action_date = models.DateField(blank=True, null=True)
    happened = models.BooleanField(blank=True, null=True)
    record_notes = models.CharField(max_length=1024, null=True, blank=True)

    # bus fares
    class Meta:
        ordering = ["-action_date",'-date_recorded']

    @property
    def duration(self):
        if self.action_start_time is not None and self.action_end_time is not None:
            t1 = self.action_start_time
            t2 = self.action_end_time
            d1 = timedelta(hours=t1.hour, minutes=t1.minute,
                           seconds=t1.second)
            d2 = timedelta(hours=t2.hour, minutes=t2.minute,
                           seconds=t2.second)
            return f"{(((d2-d1).seconds)/60):.2f}" + " min"
        
        return None
        
    @property
    def what_to_print(self):
        if self.related_item.item_type == "qty":
            return f"{self.quantity} {self.related_item.unit}"
        if self.related_item.item_type == "inst":
            return f"{str(self.action_end_time)}"
        if self.related_item.item_type == "bool":
            return "Yes" if self.happened else "No"
    
    def __str__(self):
        # return f"{self.related_item} | {str(self.date_recorded)}"
        return f"{self.related_item.record_string} | {self.what_to_print} {'| ' + self.duration   if self.duration else ''}"