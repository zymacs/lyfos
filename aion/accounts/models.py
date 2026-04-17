from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from forexchange.models import Currency
from entity.models import Entity


class Account:
    """
    That's equity account, asset account, liability account
    - name
    - currency
    - current_value
    
    """
    pass


class AssetType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    owner = models.ForeignKey(Entity, on_delete=models.SET_NULL, null=True, blank=True)
    asset_type  = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    current_value = models.DecimalField(default=0.0, decimal_places=2, max_digits=1000)

    # Generic foreign key fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    asset = GenericForeignKey('content_type', 'object_id')    
    
    @property
    def total_value(self):
        pass

    def __str__(self):
        return str(self.asset_type)


    

class CashAsset(models.Model):
    asset_type = models.ForeignKey(AssetType, on_delete=models.SET_NULL, null=True, blank=True)
    asset_nickname = models.CharField(max_length=100, null=True, blank=True)
    currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.SET_NULL)
    managing_entity = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.SET_NULL)
    current_value = models.DecimalField(default=0.0, decimal_places=2, max_digits=1000, null=True, blank=True)

    assets = GenericRelation(
        'Asset',
        content_type_field = 'content_type',
        object_id_field = 'object_id',
        related_query_name = 'cash_asset'
    )

    def save(self, *args, **kwargs):
        
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # check if type is not already available in assets before saving
            available_asset_types = [a.asset_type for a in Asset.objects.all()]
            if len(available_asset_types) != len(set([*available_asset_types, self.asset_type])):
                self.assets.create(
                asset_type=self.asset_type
                )

    def __str__(self):
        return self.asset_nickname
           
    


class CryptoAsset(models.Model):
    asset_type = models.ForeignKey(AssetType, on_delete=models.SET_NULL, null=True, blank=True)
    asset_nickname = models.CharField(max_length=100, null=True, blank=True)
    currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.SET_NULL)
    managing_entity = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.SET_NULL)
    current_value = models.DecimalField(default=0.0, decimal_places=2, max_digits=1000, null=True, blank=True)
    assets = GenericRelation(
        'Asset',
        content_type_field = 'content_type',
        object_id_field = 'object_id',
        related_query_name = 'crypto_asset'
    )

    def save(self, *args, **kwargs):
        
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # check if type is not already available in assets before saving
            available_asset_types = [a.asset_type for a in Asset.objects.all()]
            if len(available_asset_types) != len(set([*available_asset_types, self.asset_type])):
                self.assets.create(
                asset_type=self.asset_type
                )

    def transact(self, other_party=''):
        pass



    def __str__(self):
        return self.asset_nickname
    

    
class BankAsset(models.Model): # physical banks, digital banks, all banks
    asset_type = models.ForeignKey(AssetType, on_delete=models.SET_NULL, null=True, blank=True)
    asset_nickname = models.CharField(max_length=100)
    currency = models.ForeignKey(Currency, null=True, blank=True, on_delete=models.SET_NULL)
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField(null=True, blank=True)
    managing_entity = models.ForeignKey(Entity, null=True, blank=True, on_delete=models.SET_NULL)
    current_value = models.DecimalField(default=0.0, decimal_places=2, max_digits=1000, null=True, blank=True)
    assets = GenericRelation(
        'Asset',
        content_type_field = 'content_type',
        object_id_field = 'object_id',
        related_query_name = 'bank_asset'
    )

    def __str__(self):
        return self.asset_nickname
    
    def save(self, *args, **kwargs):
        
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # check if type is not already available in assets before saving
            available_asset_types = [a.asset_type for a in Asset.objects.all()]
            if len(available_asset_types) != len(set([*available_asset_types, self.asset_type])):
                self.assets.create(
                asset_type=self.asset_type
                )

# asset transactions

class Equity:
    name = ''
    currency = ''


class LiabilityType:
    pass
    
class Liability:
    pass

class Loan:
    """
    is an account
    - from: who lent the money or what entity
    - date:
    - due_date:
    """
    pass

class AmoritizationPlan:
    pass

class AmoritizationTable:
    pass


class TransactionType(models.Model):
    pass # loan, expense, internal transfer, income (gift, salary

class Transaction(models.Model):
    # transaction_type = models.ForeignKey(TransactionType,on_delete=models.PROTECT)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    from_account = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name='from_account')
    to_account = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name='to_account')
    fx_rate = models.DecimalField(default=1, decimal_places=2, max_digits=1000)


