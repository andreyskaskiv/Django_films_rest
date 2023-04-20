from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from movie.models import Movie
from movie.serializers import MoviesSerializer


class MovieApiTestCase(APITestCase):
    def setUp(self):
        self.movie_1 = Movie.objects.create(title='Loki',
                                            tagline='Glorious Purpose, King',
                                            year=2021)
        self.movie_2 = Movie.objects.create(title='Hawkeye',
                                            tagline='Holiday season, the best gifts are decorated with a bow',
                                            year=2021)
        self.movie_3 = Movie.objects.create(title='Marvel One-Shot: All Hail the King',
                                            tagline='All Hail the King',
                                            year=2014)

    def test_01_get(self):
        url = reverse('movie-list')
        response = self.client.get(url)

        serializer_data = MoviesSerializer([self.movie_1, self.movie_2, self.movie_3], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_02_get_filter(self):
        url = reverse('movie-list')
        response = self.client.get(url, data={'year': 2021})
        serializer_data = MoviesSerializer([self.movie_1,
                                           self.movie_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_03_get_search(self):
        url = reverse('movie-list')
        response = self.client.get(url, data={'search': 'King'})
        serializer_data = MoviesSerializer([self.movie_1,
                                           self.movie_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

