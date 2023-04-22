from django.db.models import Avg

from movie.models import UserMovieRelation


def set_rating(movie):
    """Rating setting function"""
    rating = UserMovieRelation.objects.filter(movie=movie).aggregate(rating=Avg('rate')).get('rating')
    movie.rating = rating
    movie.save()
