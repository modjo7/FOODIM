from django.db import models
from inventory.models import Stock

#contains items
class Item(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=150)
    
    # DEV : DecimalField can be considered, Picture need to be added. 
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    carbohydrate = models.IntegerField(default=0)
    vitamin = models.IntegerField(default=0)
    desc = models.CharField(max_length=200)
    picture = models.ImageField(null=True, blank=True, upload_to="images/")
    # End  
    
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name


#contains the purchase articles made
class PurchaseArticle(models.Model):
    articleno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)

    item = models.ForeignKey(Item, on_delete = models.CASCADE, related_name='purchaseitem')

    def __str__(self):
	    return "Article No: " + str(self.articleno)

    def get_items_list(self):
        return PurchaseItem.objects.filter(articleno=self)

    def get_total_price(self):
        purchaseitems = PurchaseItem.objects.filter(articleno=self)
        total = 0
        for item in purchaseitems:
            total += item.totalprice
        return total

#contains the purchase stocks made
class PurchaseItem(models.Model):
    articleno = models.ForeignKey(PurchaseArticle, on_delete = models.CASCADE, related_name='purchasearticleno')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='purchaseitem')
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)

    def __str__(self):
	    return "Article No: " + str(self.articleno.articleno) + ", Item = " + self.stock.name

#contains the other details in the purchases article
class PurchaseArticleDetails(models.Model):
    articleno = models.ForeignKey(PurchaseArticle, on_delete = models.CASCADE, related_name='purchasedetailsarticleno')

    title = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
	    return "Article No: " + str(self.articleno.articleno)


#contains the sale articles made
class SaleArticle(models.Model):
    articleno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
	    return "Article No: " + str(self.articleno)

    def get_items_list(self):
        return SaleItem.objects.filter(articleno=self)
        
    def get_total_price(self):
        saleitems = SaleItem.objects.filter(articleno=self)
        total = 0
        for item in saleitems:
            total += item.totalprice
        return total

#contains the sale stocks made
class SaleItem(models.Model):
    articleno = models.ForeignKey(SaleArticle, on_delete = models.CASCADE, related_name='salearticleno')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='saleitem')
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)

    def __str__(self):
	    return "Article No: " + str(self.articleno.articleno) + ", Item = " + self.stock.name

#contains the other details in the sales article
class SaleArticleDetails(models.Model):
    articleno = models.ForeignKey(SaleArticle, on_delete = models.CASCADE, related_name='saledetailsarticleno')

    address = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
	    return "Article No: " + str(self.articleno.articleno)
