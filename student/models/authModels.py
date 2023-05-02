from django.db import models

class Student(models.Model):

    SPECIALISATIONS = (
        ('AI', 'Artificial Intellignce & Data Science'),
        ('CS', 'Cyber Security'),
        ('DA', 'Data Administration'),
        ('GD', 'Graphic Design'),
        ('HO', 'Hardware & Operating Systems'),
        ('IS', 'Information Systems'),
        ('NC', 'Network Configuration'),
        ('SD', 'Software Development')
    )

    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=100, unique=True)

    # ------------- prediction fields --------------
    specialisation = models.CharField(max_length=50, choices=SPECIALISATIONS)
    compatibility_scores = models.JSONField(default=list    )

    # ------------- auth fields --------------
    user_token = models.CharField(max_length=200, null=True)
    last_active = models.CharField(max_length=200, null=True)

    first_pet = models.CharField(max_length=200, null=True)
    childhood_street = models.CharField(max_length=200, null=True)
    first_teacher = models.CharField(max_length=200, null=True)
    favourite_flavour = models.CharField(max_length=200, null=True)
    childhod_nickname = models.CharField(max_length=200, null=True)
    first_phone = models.CharField(max_length=200, null=True)

    # ------------- news setting fields -------------------
    news_history = models.JSONField(default=list, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def getId(self):
        return self.id
