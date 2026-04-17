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


