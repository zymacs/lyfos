from django.contrib import admin

from .models import AssetType, Asset, CashAsset, BankAsset, CryptoAsset


imported_models = [AssetType, Asset, CashAsset, BankAsset, CryptoAsset]

for asset in imported_models:
    admin.site.register(asset)
