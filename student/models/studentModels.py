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
    specialisation_score = models.FloatField(default=0.0)
    compatibility_scores = models.JSONField(default=list)

    # ------------- auth fields --------------
    user_token = models.CharField(max_length=200, null=True)
    last_active = models.CharField(max_length=200, null=True)

    childhod_nicknamefirst_pet = models.CharField(max_length=200, null=True)
    childhood_street = models.CharField(max_length=200, null=True)
    first_teacher = models.CharField(max_length=200, null=True)
    favourite_flavour = models.CharField(max_length=200, null=True)
    childhod_nickname = models.CharField(max_length=200, null=True)
    first_phone = models.CharField(max_length=200, null=True)

    # ------------- news setting fields -------------------
    news_history = models.JSONField(default=list, null=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    @property
    def studentId(self):
        return self.id

    @property
    def specialisation(self):
        return self.specialisation

    @property
    def securityQuestions(self):
        answers = {}
        answers['name'] = self.first_name + ' ' + self.last_name
        answers['email'] = self.email
        answers['first_pet'] = self.first_pet
        answers['childhood_street'] = self.childhood_street
        answers['first_teacher'] = self.first_teacher
        answers['favourite_flavour'] = self.favourite_flavour
        answers['childhod_nickname'] = self.childhod_nickname
        answers['first_phone'] = self.first_phone
        return answers
