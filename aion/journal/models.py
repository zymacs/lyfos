from django.db import models

# Create your models here.

class Journal(models.Model):
    journal_date = models.DateField(auto_now_add=True)
    journal_time = models.TimeField(auto_now_add=True)
    last_modificication_date = models.DateTimeField(null=True, blank=True, auto_now=True)
    journal_content = models.TextField()
    
    

    def __str__(self):
        return f'{self.journal_date} {self.journal_time}'
