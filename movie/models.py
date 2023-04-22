from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    """Movie"""
    title = models.CharField(max_length=255)
    tagline = models.CharField("tagline", max_length=100, default='')
    description = models.TextField(null=True, blank=True)
    year = models.PositiveSmallIntegerField("Release date", default=2019)

    readers = models.ManyToManyField(User, through='UserMovieRelation',
                                     related_name='movie')

    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)

    def __str__(self):
        return f'Id {self.id}: {self.title}'

    class Meta:
        verbose_name = 'movie'
        verbose_name_plural = 'movies'


class UserMovieRelation(models.Model):
    """ like, in_bookmarks, rate """
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f' {self.user.username}: {self.movie.title},' \
               f' LIKE: {self.like}, IN_bookmarks: {self.in_bookmarks}, RATE: {self.rate}'

    def __init__(self, *args, **kwargs):
        super(UserMovieRelation, self).__init__(*args, **kwargs)
        self.old_rate = self.rate

    def save(self, *args, **kwargs):
        creating = not self.pk

        super().save(*args, **kwargs)

        if self.old_rate != self.rate or creating:
            from movie.utils import set_rating
            set_rating(self.movie)
