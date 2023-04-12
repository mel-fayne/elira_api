from django.db import models

# Create your models here.
class Student(models.Model):
  
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=100, unique=True)

    # ------------- auth fields --------------
    user_token = models.CharField(max_length=200, null=True)
    last_active = models.CharField(max_length=200, null = True)
    isVerified = models.BooleanField(default=False)
    verify_otp = models.IntegerField(null=True)
    reset_otp = models.IntegerField(null=True)
    reset_expiry = models.DateTimeField(null=True)

    # ------------- news setting fields -------------------
    news_history = models.JSONField(default=list, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def getId(self):
        return self.id
    
    def getIsVerified(self):
        return self.isVerified
    
    def getVerifyCode(self):
        return self.verify_otp
    
    def getOTP(self):
        return self.reset_otp
    
    def getOTPTime(self):
        return self.reset_expiry
    
class TechnicalProfile(models.Model):

    student_id = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    git_username = models.CharField(max_length=50)
    total_commits = models.IntegerField(default=0)
    total_prs = models.IntegerField(default=0)
    current_streak  = models.IntegerField(default=0)
    top_languages = models.JSONField(default=dict)
    repos = models.JSONField(default=dict)
    technical_score = models.FloatField(default=0.0)
    specialisation_rank = models.JSONField(default=dict)

    def __str__(self):
        return self.git_username