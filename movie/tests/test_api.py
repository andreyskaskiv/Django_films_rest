from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from movie.models import Movie
from movie.serializers import MoviesSerializer


class MovieApiTestCase(APITestCase):
    def test_get(self):
        movie_1 = Movie.objects.create(title='Loki',
                                       tagline='Glorious Purpose')
        movie_2 = Movie.objects.create(title='Hawkeye',
                                       tagline='Holiday season, the best gifts are decorated with a bow')

        url = reverse('movie-list')
        response = self.client.get(url)

        serializer_data = MoviesSerializer([movie_1, movie_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
