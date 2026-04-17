from django.contrib import admin

# Register your models here.

from .models import Entity, EntityType

admin.site.register(Entity)
admin.site.register(EntityType)

