import hashlib
import os
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
    password = models.CharField(max_length=500)

    # ------------- prediction fields --------------
    specialisation = models.CharField(max_length=50, choices=SPECIALISATIONS, null=True)
    specialisation_score = models.FloatField(default=0.0)
    compatibility_scores = models.JSONField(default=list)

    # ------------- progress fields --------------
    project_wishlist = models.JSONField(default=list)
    spec_roadmaps = models.JSONField(default=list)

    # ------------- auth fields --------------
    user_token = models.CharField(max_length=200, null=True)
    last_active = models.CharField(max_length=200, null=True)

    first_pet = models.CharField(max_length=50, null=True, blank=True)
    childhood_street = models.CharField(max_length=50, null=True, blank=True)
    first_teacher = models.CharField(max_length=50, null=True, blank=True)
    favourite_flavour = models.CharField(max_length=50, null=True, blank=True)
    childhod_nickname = models.CharField(max_length=50, null=True, blank=True)
    first_phone = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    @property
    def studentId(self):
        return self.id

    @property
    def studentSpec(self):
        return self.specialisation
    
    @property
    def projectWishList(self):
        return self.project_wishlist
    
    @property
    def specMaps(self):
        return self.spec_roadmaps

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

    def set_password(self, raw_password):
        """
        Set the password for the user. The raw password will be hashed before
        storing it in the database.
        """
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwd_hash = hashlib.pbkdf2_hmac('sha256', raw_password.encode('utf-8'), salt, 100000)
        pwd_hash = pwd_hash.hex()
        self.password = f"{salt.decode('ascii')}:{pwd_hash}"


    def check_password(self, raw_password):
        """
        Check if the provided password matches the user's hashed password.
        """
        salt, pwd_hash = self.password.split(':')
        pwd_input_hash = hashlib.pbkdf2_hmac('sha256', raw_password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwd_input_hash = pwd_input_hash.hex()
        return pwd_input_hash == pwd_hash
