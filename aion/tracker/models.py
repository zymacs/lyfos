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

    class Meta:
        ordering = ['-name']

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
    

