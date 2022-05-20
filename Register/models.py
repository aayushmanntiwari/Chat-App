from enum import unique
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.crypto import get_random_string
from phone_field import PhoneField





# Create your models here.
class UserProfile(models.Model):
    middle_name = models.CharField(max_length=50,blank=True,null=True)
    birthday = models.DateField(blank=False,null=False)
    country = models.CharField(max_length=20,blank=True,null=True)
    phone_number = models.CharField(max_length=30,unique=True,blank=False,null=False)
    phone_number_verified = models.BooleanField(default=False)
    two_factor_check = models.BooleanField(default=False)
    api_key = models.TextField(blank=True,null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    
    def name(self):
        if self.user is not None:
            return self.user.username


    



