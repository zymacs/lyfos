from django.db import models

# Create your models here.

meal_types = [
    ('break','breakfast'),
    ('lunch','lunch'),
    ('supper','supper'),
    ('snack','snack')
]


class MealLog(models.Model):
    log_date = models.DateField(auto_now_add=True)
    log_time = models.TimeField(null=True, blank=True)
    meal_type = models.CharField(choices=meal_types, default='snack')
    what_was_eaten = models.TextField()
    extra_notes = models.TextField(null=True, blank=True)


    def __str__(self):
        return f'{self.log_date} | {self.log_time} | {self.meal_type}'
