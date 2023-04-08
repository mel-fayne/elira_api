from django.db import models

# Create your models here.
class Student(models.Model):
  
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=200, unique=True)

    # ------------- auth fields --------------
    user_token = models.CharField(max_length=200, null=True)
    last_active = models.CharField(max_length=200, null = True)
    reset_otp = models.IntegerField(null=True)
    reset_time = models.DateTimeField(null=True)

    # ------------- news setting fields -------------------
    news_history = models.JSONField(default=list, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def getId(self):
        return self.id
    
    def getOTP(self):
        return self.reset_otp
    
    def getOTPTime(self):
        return self.reset_time
    