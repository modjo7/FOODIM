from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True) # For hiding information, it has to be filled with current user name as default input.
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    signupday = models.DateField(auto_now=True)
    password_hint = models.CharField(max_length=30)
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    carbohydrate = models.IntegerField(default=0)
    vitamin = models.IntegerField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['birthday', 'password_hint']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class ConsumedData(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150)
    protein = models.IntegerField(default=0)
    fat = models.IntegerField(default=0)
    carbohydrate = models.IntegerField(default=0)
    vitamin = models.IntegerField(default=0)
    def __str__(self):
        return self.username
