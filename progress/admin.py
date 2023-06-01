from django.contrib import admin
from . import models

admin.site.register(models.AppData)
admin.site.register(models.ProjectIdea)
admin.site.register(models.SpecRoadmap)
admin.site.register(models.StudentProject)