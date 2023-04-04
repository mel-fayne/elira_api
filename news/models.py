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


class NewsGroup(models.Model):

    student_ids = models.JSONField(default=list)

    def __str__(self):
        return self.id
