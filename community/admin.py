from django.contrib import admin
from .models import (
    Item, 
    PurchaseArticle, 
    PurchaseItem,
    PurchaseArticleDetails, 
    SaleArticle, 
    SaleItem,
    SaleArticleDetails
)

admin.site.register(Item)
admin.site.register(PurchaseArticle)
admin.site.register(PurchaseItem)
admin.site.register(PurchaseArticleDetails)
admin.site.register(SaleArticle)
admin.site.register(SaleItem)
admin.site.register(SaleArticleDetails)