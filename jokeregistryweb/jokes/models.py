from django.conf import settings
from django.db import models


class Joke(models.Model):

    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField()
    link = models.URLField(null=True, blank=True)
