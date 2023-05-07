from django.db import models

from student.models.authModels import Student


INDUSTRIES = ['ai_industry', 'cs_industry', 'da_industry', 'gd_industry',
              'ho_industry', 'is_industry', 'na_industry', 'sd_industry']

class WorkExpProfile(models.Model):
    INTERNED = (
        (0, 0),
        (1, 1)
    )

    student_id = models.OneToOneField(
        Student, null=True, on_delete=models.CASCADE)

    internships_no = models.IntegerField(default=0)
    time_spent = models.IntegerField(default=0)
    ai_industry = models.IntegerField(choices=INTERNED, default=0)
    cs_industry = models.IntegerField(choices=INTERNED, default=0)
    da_industry = models.IntegerField(choices=INTERNED, default=0)
    gd_industry = models.IntegerField(choices=INTERNED, default=0)
    ho_industry = models.IntegerField(choices=INTERNED, default=0)
    is_industry = models.IntegerField(choices=INTERNED, default=0)
    na_industry = models.IntegerField(choices=INTERNED, default=0)
    sd_industry = models.IntegerField(choices=INTERNED, default=0)

    @property
    def wxProfileId(self):
        return self.id
    
    @property
    def internshipsNo(self):
        return self.internships_no
    
    @property
    def timeSpent(self):
        return self.time_spent
    

class WorkExperience(models.Model):
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
        ('sd_industry', 'Software Development'),
        ('na_industry', 'Networking'),
        ('ai_industry', 'Data Science & AI'),
        ('cs_industry', 'Cyber Security'),
        ('da_industry', 'Database Administration'),
        ('ho_industry', 'Hardware & Operating Systems'),
        ('is_industry', 'Information Systems'),
        ('gd_industry', 'Graphics & Design')
    )

    wx_profile = models.ForeignKey(
        WorkExpProfile, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    employment_type = models.CharField(max_length=50, choices=EMP_TYPE)
    company_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    location_type = models.CharField(max_length=50, choices=LOC_TYPE)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    time_spent = models.IntegerField(default=0)
    industry = models.CharField(max_length=50, choices=INDUSTRIES)
    skills = models.JSONField(default=dict)

    def __str__(self):
        return self.title
    
    @property
    def wxProfileId(self):
        return self.wx_profile
    
    @property
    def timeSpent(self):
        return self.time_spent
    
    @property
    def industry(self):
        return self.industry
