from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    """Movie"""
    title = models.CharField(max_length=255)
    tagline = models.CharField("tagline", max_length=100, default='')
    description = models.TextField(null=True, blank=True)
    year = models.PositiveSmallIntegerField("Release date", default=2019)

    def __str__(self):
        return f'Id {self.id}: {self.title}'

    class Meta:
        verbose_name = 'movie'
        verbose_name_plural = 'movies'

