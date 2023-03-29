from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Student(AbstractUser):

    user_token = models.CharField(max_length=200, null=True)
    last_active = models.CharField(max_length=200, null = True)
    reset_key = models.CharField(max_length=200, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def getId(self):
        return self.id
    
    def getName(self):
        return self.first_name + ' ' + self.last_name