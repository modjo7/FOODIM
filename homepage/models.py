from django.contrib.auth.models import AbstractUser
from django.db import models
#from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _


from .managers import CustomUserManager


class CustomUser(AbstractUser):
    # For hiding information, it has to be filled with current user name as default input.
    username = models.CharField(max_length=30, unique=True)
    # False options for futher modification (there is a null issue)
    birthday = models.DateField(auto_now=False, auto_now_add=False)

    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    carbohydrate = models.IntegerField(default=0)
    vitamin = models.IntegerField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['birthday']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
