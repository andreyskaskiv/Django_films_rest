from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from movie.models import Movie, UserMovieRelation
from movie.serializers import MoviesSerializer


class MovieSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1', email='user1@gmail.com')
        user2 = User.objects.create(username='user2', email='user2@gmail.com')
        user3 = User.objects.create(username='user3', email='user3@gmail.com')

        self.movie_1 = Movie.objects.create(title='Loki',
                                            tagline='Glorious Purpose, King',
                                            year=2021)
        self.movie_2 = Movie.objects.create(title='Hawkeye',
                                            tagline='Holiday season, the best gifts are decorated with a bow',
                                            year=2021)

        UserMovieRelation.objects.create(user=user1, movie=self.movie_1, like=True,
                                         rate=5)
        UserMovieRelation.objects.create(user=user2, movie=self.movie_1, like=True,
                                         rate=5)
        UserMovieRelation.objects.create(user=user3, movie=self.movie_1, like=True,
                                         rate=4)

        UserMovieRelation.objects.create(user=user1, movie=self.movie_2, like=True,
                                         rate=3)
        UserMovieRelation.objects.create(user=user2, movie=self.movie_2, like=True,
                                         rate=4)
        UserMovieRelation.objects.create(user=user3, movie=self.movie_2, like=False)

        queryset = Movie.objects.all().annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            rating=Avg('usermovierelation__rate')
        ).order_by('id')

        data = MoviesSerializer(queryset, many=True).data
        expected_data = [
            {
                'id': self.movie_1.id,
                'title': 'Loki',
                'tagline': 'Glorious Purpose, King',
                'description': None,
                'year': 2021,
                'readers': [
                    {
                        "username": "user1",
                        "email": "user1@gmail.com"
                    },
                    {
                        "username": "user2",
                        "email": "user2@gmail.com"
                    },
                    {
                        "username": "user3",
                        "email": "user3@gmail.com"
                    },
                ],
                'annotated_likes': 3,
                'rating': '4.67',
            },
            {
                'id': self.movie_2.id,
                'title': 'Hawkeye',
                'tagline': 'Holiday season, the best gifts are decorated with a bow',
                'description': None,
                'year': 2021,
                'readers': [
                    {
                        "username": "user1",
                        "email": "user1@gmail.com"
                    },
                    {
                        "username": "user2",
                        "email": "user2@gmail.com"
                    },
                    {
                        "username": "user3",
                        "email": "user3@gmail.com"
                    },
                ],
                'annotated_likes': 2,
                'rating': '3.50',
            },
        ]

        # print()
        # print(f"data => {data}")
        # print(f"expected_data => {expected_data}")

        self.assertEqual(expected_data, data)
