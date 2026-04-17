from django.contrib import admin
from .models import MarketQuote, Currency

# Register your models here.

admin.site.register(MarketQuote)
admin.site.register(Currency)
