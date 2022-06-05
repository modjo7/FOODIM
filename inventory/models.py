from django.db import models

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    quantity = models.IntegerField(default=1)

    itemname = models.CharField(max_length=30)
    quantity_eat = models.IntegerField(default=0) # user can modify this value in the list window
    username = models.CharField(max_length=30) # For hiding information, it has to be filled with current user name as default input.
    expdate = models.DateField(auto_now=False, auto_now_add=False, default="2022-06-08") # False options for futher modification (there is a null issue)
    timeleft = models.IntegerField(default=0) # no user input
    desc = models.CharField(max_length=300)
    photo = models.ImageField(null=True, blank=True, upload_to="images/")

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name