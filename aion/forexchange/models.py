from django.db import models

# Create your models here.
# api key: alphavantage: 4WGXZCV5M5F79SXN
# marketstack: 71b3b1975ae52cabbf57bc826a83d8d8
# alpaca key: PKNYPNMRWZO5UYO5E6CEDMRV7M
# alpaca sec: 6Z1eduoHJCQ1DQTkWNEn294edT7WmRpBdNqA1Wu85zCy
"""
records for exchange rates when i translate money (for the exchange entity(entered by me) and from the internet(various sources))
info about money gained or lost from doing forexchange: this is to be implemented on the account records side
means to easily translate money between currencies: Answer such easy questions as "What is X in this currency or
What is the most valuable currency"
Flexibility to handle both fiat and crypto
Records for daily exchange rates for the currencies I use often if not all currencies available
Track institutions forex rates so to tell which is more affordable than the other

Building this:
- list and describe available services
  - primary
    - Foreign exchange service (primary)
       - Including fiat and crypto (but we start with just forex)
  - Others
    - tracking service
       - tracking some pair means
- list data thatll be needed
    - for the forx service
      - major pairs exchange data
         - (from the market makers vantage point) pair say eur/usd, bid price, ask price, date, broker
         - also need a setting for frequency of updates
- model storage structure
- list output format for each service
- gather providers
- write scripts to interact with providers
- collect base data from providers
- write scripts to automate data updates to keep exchange data up to date
- write interfaces to provide services from the now available data


-- mvp
- manual entry

-- next steps (still very very basic, auto updates every day)
- a flat rate api with forexrateapi: keys: 1db238ac472dacc18c34d95e50007c1f , site: https://forexrateapi.com/dashboard

-- next steps (bid ask price from other brokers)

"""

currency_types = [
    ('commodity_money','Commodity Money'),
    ('fiat_money','Fiat Money'),
    ('fiduciary_money', 'Fiduciary Money'),
    ('crypto','Cryptocurrency')
]



class Currency(models.Model):
    currency_name = models.CharField(max_length=20)
    currency_symbol = models.CharField(max_length=10)
    currency_type = models.CharField(max_length=100, choices=currency_types)

    class Meta:
        verbose_name_plural = 'currencies'
    
    def __str__(self):
        return self.currency_symbol


# instrument type specific tables for holding type centric data

class MarketQuote(models.Model):
    symbol = models.CharField(max_length=20)# eur/usd eur/btc apple
    instrument_type = models.CharField(max_length=20, default="currency_pair") 
    bid_price = models.FloatField(null=True, blank=True)
    ask_price = models.FloatField(null=True, blank=True)
    flat_rate = models.FloatField(null=True, blank=True)
    date = models.DateTimeField()
    source = models.CharField(max_length=100)
    is_flat_rate = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.date} | {self.symbol} | {self.flat_rate or 'NA'} | {self.bid_price or 'NA'} | {self.ask_price or 'NA'}"



class MarketUtils:

    def get_rate(symbol_pair):
        entries = MarketQuote.objects.filter(symbol__contains=symbol_pair)
        if len(entries) > 0:
            target_entry =  entries[0]
            rate = target_entry.flat_rate
            return rate
        else:
            return None
