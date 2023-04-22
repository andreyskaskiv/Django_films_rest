from django.contrib.auth.models import User
from django.test import TestCase

from movie.models import Movie, UserMovieRelation
from movie.utils import set_rating


class SetRatingTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='user1', email='user1@gmail.com')
        user2 = User.objects.create(username='user2', email='user2@gmail.com')
        user3 = User.objects.create(username='user3', email='user3@gmail.com')

        self.movie_1 = Movie.objects.create(title='Loki',
                                            tagline='Glorious Purpose, King',
                                            year=2021)

        UserMovieRelation.objects.create(user=user1, movie=self.movie_1, like=True,
                                         rate=5)
        UserMovieRelation.objects.create(user=user2, movie=self.movie_1, like=True,
                                         rate=5)
        UserMovieRelation.objects.create(user=user3, movie=self.movie_1, like=True,
                                         rate=4)

    def test_ok(self):
        set_rating(self.movie_1)
        self.movie_1.refresh_from_db()
        self.assertEqual('4.67', str(self.movie_1.rating))
