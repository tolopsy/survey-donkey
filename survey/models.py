from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType

from .subroutines import random_id
from .fields import OrderField


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

    class Meta:
        ordering = ['-date_updated']

    def __str__(self):
        return "%s - %s" % (self.creator.username, self.title)


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    body = models.TextField()
    help_label = models.CharField(max_length=100, blank=True, null=True) # To include hint (if necessary) on how to answer question

    answer_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    order = OrderField(blank=True, for_fields=['survey'])

    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return "Question %s" % self.order
