from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User
# Create your models here.


class users_table(models.Model):
    username = models.CharField( max_length=30,unique = True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30,unique= True)
    tel = PhoneField(blank=True, help_text='Contact phone number',unique = True)
    DOB = models.DateField()
    password = models.CharField(max_length=32)
    Resume = models.FileField(upload_to='documents/')
    gender = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
