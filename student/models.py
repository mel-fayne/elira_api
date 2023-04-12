from django.db import models

# Create your models here.


class Student(models.Model):

    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=100, unique=True)

    # ------------- auth fields --------------
    user_token = models.CharField(max_length=200, null=True)
    last_active = models.CharField(max_length=200, null=True)
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

    student_id = models.ForeignKey(
        Student, null=True, on_delete=models.CASCADE)
    git_username = models.CharField(max_length=50)
    total_commits = models.IntegerField(default=0)
    total_prs = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    top_languages = models.JSONField(default=dict)
    repos = models.JSONField(default=dict)
    technical_score = models.FloatField(default=0.0)
    specialisation_rank = models.JSONField(default=dict)

    def __str__(self):
        return self.git_username


class WorkExpProfile(models.Model):
    EMP_TYPE = (
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Internship', 'Internship')
    )

    LOC_TYPE = (
        ('Online', 'Online'),
        ('Hybrid', 'Hybrid'),
        ('On-Site', 'On-Site')
    )

    INDUSTRIES = (
        ('Software Development', 'Software Development'),
        ('Networking', 'Networking'),
        ('Data Science & AI', 'Data Science & AI'),
        ('Cyber Security', 'Cyber Security'),
        ('Database Administration', 'Database Administration'),
        ('IT & Support', 'IT & Support'),
        ('Mobile Development', 'Mobile Development'),
        ('Web Development', 'Web Development'),
        ('Design', 'Design'),
    )

    student_id = models.ForeignKey(
        Student, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=100, choices=EMP_TYPE)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    location_type = models.CharField(max_length=100, choices=LOC_TYPE)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    industry = models.CharField(max_length=100, choices=INDUSTRIES)
    skills = models.JSONField(default=dict)
    work_exp_score = models.FloatField(default=0.0)
    specialisation_rank = models.JSONField(default=dict)

    def __str__(self):
            return self.title