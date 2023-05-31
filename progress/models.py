from django.db import models


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

class ProjectIdea(models.Model):
    LEVELS = (
        ('B', 'Beginner'),
        ('I', 'Intermediate'),
        ('A', 'Advanced'),
    )

    name = models.CharField(max_length=150, null=True)
    description = models.CharField(max_length=300, null=True)
    specialisation = models.CharField(max_length=50, choices=SPECIALISATIONS)
    level = models.CharField(max_length=50, choices=LEVELS)

    def __str__(self):
        return self.name

    @property
    def ideaSpec(self):
        return self.specialisation

    @property
    def ideaLevel(self):
        return self.level

class AppData(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, null=True)
    current_value = models.IntegerField(default=0)

    @property
    def currentIndex(self):
        return self.current_value
