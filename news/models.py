from django.db import models

class NewsPiece(models.Model):

    source = models.CharField(max_length=50)
    source_img = models.CharField(max_length=50)
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=800)
    header_img = models.CharField(max_length=800)
    publication = models.CharField(max_length=50)
    tags = models.JSONField(default=list)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def newsTags(self):
        return self.tags

class TechEvent(models.Model):

    source = models.CharField(max_length=50)
    isOnline = models.BooleanField()
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=800)
    img = models.CharField(max_length=800)
    location = models.CharField(max_length=200)
    organiser = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    format = models.JSONField(default=list)
    themes = models.JSONField(default=list)

    def __str__(self):
        return self.title

class TechJob(models.Model):

    source = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=800)
    job_logo = models.CharField(max_length=800)
    description = models.CharField(max_length=1000)
    company = models.CharField(max_length=200)
    posted = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    areas = models.JSONField(default=list)

    def __str__(self):
        return self.title

    @property
    def jobAreas(self):
        return self.areas
