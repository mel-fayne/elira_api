from django.db import models

# Create your models here.
class Student(models.Model):
  
    first_name = models.CharField(max_length=50)
    last_name_name = models.CharField(max_length=50)
    email = models.CharField(max_length=200, unique=True)

    # ------------- auth fields --------------
    user_token = models.CharField(max_length=200, null=True)
    last_active = models.CharField(max_length=200, null = True)
    reset_key = models.CharField(max_length=200, null=True)

    # ------------- news setting fields -------------------
    news_history = models.JSONField(default=list, null=True)

    def __str__(self):
        return self.email