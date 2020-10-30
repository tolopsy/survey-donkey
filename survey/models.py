from django.db import models
from django.contrib.auth.models import AbstractUser

from .subroutines import random_id  # to create unique id for each survey


class SurveyUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Survey(models.Model):
    creator = models.ForeignKey(SurveyUser, on_delete=models.CASCADE, related_name="surveys")
    unique_id = models.CharField(max_length=50, default=random_id, unique=True)  # to be used as part of the url
    title = models.CharField(max_length=100)
    description = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.creator.username, self.title)