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


    
class GenericLink(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="generic_links", blank=True, null=True)
    link_name = models.CharField(max_length=200)
    link_url = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.link_name} | {self.link_url}"
