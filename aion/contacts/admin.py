from django.contrib import admin

from .models import Email, SocialMediaHandle, PhoneNumber, GenericLink

# Register your models here.

admin.site.register(SocialMediaHandle)
admin.site.register(PhoneNumber)
admin.site.register(Email)
admin.site.register(GenericLink)
