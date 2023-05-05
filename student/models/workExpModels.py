from django.db import models

from student.models.authModels import Student

class WorkExpProfile(models.Model):
    student_id = models.OneToOneField(
        Student, null=True, on_delete=models.CASCADE)

    def getId(self):
        return self.id


class WorkExp(models.Model):
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
        ('nc_industry', 'Networking'),
        ('ai_industry', 'Data Science & AI'),
        ('cs_industry', 'Cyber Security'),
        ('da_industry', 'Database Administration'),
        ('ho_industry')
        ('gd_industry')
        ()
    )
    wx_profile = models.ForeignKey(
        WorkExpProfile, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=100, choices=EMP_TYPE)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    location_type = models.CharField(max_length=100, choices=LOC_TYPE)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    industry = models.CharField(max_length=100, choices=INDUSTRIES)
    skills = models.JSONField(default=dict)

    def __str__(self):
        return self.title