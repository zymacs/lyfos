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
