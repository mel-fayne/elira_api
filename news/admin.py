from django.contrib import admin
from . import models

admin.site.register(models.NewsPiece)
admin.site.register(models.TechEvent)
admin.site.register(models.TechJob)