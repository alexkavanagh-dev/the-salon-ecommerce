from django.db import models

# Create your models here.


class FAQ(models.Model):
    """
    A FAQ model for frequently asked questions to be shown on the FAQ page
    """
    question = models.CharField(max_length=100)
    answer = models.TextField()
