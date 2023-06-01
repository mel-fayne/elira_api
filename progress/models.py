from django.db import models

from student.models.studentModels import Student


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

class StudentProject(models.Model):
    STATUSES = (
        ('O', 'Ongoing'),
        ('C', 'Complete')
    )

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=300, null=True, blank=True)
    git_link = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUSES, default='O')
    progress = models.FloatField(default=0.0)
    current_step = models.IntegerField(default=1)
    steps  = models.JSONField(default=list)
    student_id = models.ForeignKey(
        Student, null=True, on_delete=models.CASCADE)
    project_idea = models.ForeignKey(
        ProjectIdea, null=True, on_delete=models.SET_NULL)


class AppData(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, null=True)
    current_value = models.IntegerField(default=0)

    @property
    def currentIndex(self):
        return self.current_value
