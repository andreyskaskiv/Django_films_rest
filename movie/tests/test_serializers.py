from django.test import TestCase

from movie.models import Movie
from movie.serializers import MoviesSerializer


class MovieSerializerTestCase(TestCase):
    def test_ok(self):
        movie_1 = Movie.objects.create(title='Loki',
                                       tagline='Glorious Purpose')
        movie_2 = Movie.objects.create(title='Hawkeye',
                                       tagline='Holiday season, the best gifts are decorated with a bow')
        data = MoviesSerializer([movie_1, movie_2], many=True).data
        expected_data = [
            {
                'id': movie_1.id,
                'title': 'Loki',
                'tagline': 'Glorious Purpose',
                'description': None,
                'year': 2019,
            },
            {
                'id': movie_2.id,
                'title': 'Hawkeye',
                'tagline': 'Holiday season, the best gifts are decorated with a bow',
                'description': None,
                'year': 2019,
            },
        ]

        # print(data)
        self.assertEqual(expected_data, data)