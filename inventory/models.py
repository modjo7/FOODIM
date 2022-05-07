from django.db import models

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    quantity = models.IntegerField(default=1)

    # DEV added

    itemname = models.CharField(max_length=30, default=0)
    quantity_eat = models.IntegerField(default=0) # user can modify this value in the list window
    username = models.CharField(max_length=30, default="modjo") # For hiding information, it has to be filled with current user name as default input.
    expdate = models.DateField(auto_now=False, auto_now_add=False, default="2022-05-30") # False options for futher modification (there is a null issue)
    timeleft = models.IntegerField(default=0) # no user input
    desc = models.CharField(max_length=300, default=0)
    # picture_stock = models.ImageField(upload_to='uploads/stock', default=0)

    # DEV test (to solve DeferredAttribute)
    # expdate2 = models.CharField(max_length=16, default="221231")  # False options for futher modification (there is a null issue)

    # END

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name