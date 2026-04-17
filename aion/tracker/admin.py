from django.contrib import admin
from .models import Unit, Category, Tag, Item, Record

# Register your models here.

admin.site.register(Unit)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Item)
admin.site.register(Record)
