import json

from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count, Case, When, Avg
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from movie.models import Movie, UserMovieRelation
from movie.serializers import MoviesSerializer


class MovieApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username', is_staff=True)

        self.movie_1 = Movie.objects.create(title='Loki',
                                            tagline='Glorious Purpose, King',
                                            year=2021)
        self.movie_2 = Movie.objects.create(title='Hawkeye',
                                            tagline='Holiday season, the best gifts are decorated with a bow',
                                            year=2021)
        self.movie_3 = Movie.objects.create(title='Marvel One-Shot: All Hail the King',
                                            tagline='All Hail the King',
                                            year=2014)

        UserMovieRelation.objects.create(user=self.user, movie=self.movie_1, like=True,
                                         rate=5)

    def test_01_get(self):
        url = reverse('movie-list')

        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(2, len(queries))

        queryset = Movie.objects.all().annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            rating=Avg('usermovierelation__rate')
        ).order_by('id')
        serializer_data = MoviesSerializer(queryset, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['rating'], '5.00')
        self.assertEqual(serializer_data[0]['annotated_likes'], 1)

    def test_02_get_filter(self):
        url = reverse('movie-list')
        response = self.client.get(url, data={'year': 2021})

        queryset = Movie.objects.filter(id__in=[self.movie_1.id, self.movie_2.id]).annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            rating=Avg('usermovierelation__rate')
        ).order_by('id')
        serializer_data = MoviesSerializer(queryset, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_03_get_search(self):
        url = reverse('movie-list')
        response = self.client.get(url, data={'search': 'King'})

        queryset = Movie.objects.filter(id__in=[self.movie_1.id, self.movie_3.id]).annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            rating=Avg('usermovierelation__rate')
        ).order_by('id')
        serializer_data = MoviesSerializer(queryset, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_04_get_ordering(self):
        url = reverse('movie-list')
        response = self.client.get(url, data={'ordering': '-year'})

        queryset = Movie.objects.annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            rating=Avg('usermovierelation__rate')
        ).order_by('-year')
        serializer_data = MoviesSerializer(queryset, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_05_POST_create(self):
        self.assertEqual(3, Movie.objects.all().count())
        url = reverse('movie-list')
        data = {
            "title": "Stranger Things",
            "tagline": "There is no end without a beginning",
            "description": "The action of the series takes place in November 1983 in the small provincial town of "
                           "Hawkins.",
            "year": 2016
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, json_data,
                                    content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Movie.objects.all().count())

    def test_06_PUT_update(self):
        url = reverse('movie-detail', args=(self.movie_1.id,))
        data = {
            "title": "New title",
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.movie_1.refresh_from_db()
        self.assertEqual("New title", self.movie_1.title)

    def test_07_DELETE(self):
        self.assertEqual(3, Movie.objects.all().count())
        url = reverse('movie-detail', args=(self.movie_1.id,))

        self.client.force_login(self.user)
        response = self.client.delete(url,
                                      content_type='application/json')

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Movie.objects.all().count())

    def test_08_get_id(self):
        url = reverse('movie-detail', args=(self.movie_1.id,))
        response = self.client.get(url)

        queryset = Movie.objects.filter(id__in=[self.movie_1.id]).annotate(
            annotated_likes=Count(Case(When(usermovierelation__like=True, then=1))),
            rating=Avg('usermovierelation__rate')
        ).order_by('id')
        serializer_data = MoviesSerializer(queryset, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data[0], response.data)

    def test_09_PUT_update_not_staff(self):
        self.user_not_staff = User.objects.create(username='test_username_not_staff', )
        url = reverse('movie-detail', args=(self.movie_1.id,))
        data = {
            "title": "New title",
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_not_staff)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.movie_1.refresh_from_db()
        self.assertEqual('Loki', self.movie_1.title)

    def test_10_PUT_update_not_login(self):
        url = reverse('movie-detail', args=(self.movie_1.id,))
        data = {
            "title": "New title",
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data,
                                   content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='Authentication credentials were not provided.',
                                                code='not_authenticated')}, response.data)
        self.movie_1.refresh_from_db()
        self.assertEqual('Loki', self.movie_1.title)

    def test_11_DELETE_not_staff(self):
        self.assertEqual(3, Movie.objects.all().count())
        self.user_not_staff = User.objects.create(username='test_username_not_staff', )
        url = reverse('movie-detail', args=(self.movie_1.id,))

        self.client.force_login(self.user_not_staff)
        response = self.client.delete(url,
                                      content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.assertEqual(3, Movie.objects.all().count())

    def test_12_DELETE_not_login(self):
        self.assertEqual(3, Movie.objects.all().count())
        url = reverse('movie-detail', args=(self.movie_1.id,))
        response = self.client.delete(url,
                                      content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='Authentication credentials were not provided.',
                                                code='not_authenticated')}, response.data)
        self.movie_1.refresh_from_db()
        self.assertEqual(3, Movie.objects.all().count())

    def test_13_POST_create_login_not_stuff(self):
        self.assertEqual(3, Movie.objects.all().count())
        self.user_not_staff = User.objects.create(username='test_username_not_staff', )
        url = reverse('movie-detail', args=(self.movie_1.id,))

        self.client.force_login(self.user_not_staff)
        response = self.client.delete(url,
                                      content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='You do not have permission to perform this action.',
                                                code='permission_denied')}, response.data)
        self.movie_1.refresh_from_db()
        self.assertEqual(3, Movie.objects.all().count())


class MoviesRelationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_username_not_stuff')

        self.movie_1 = Movie.objects.create(title='Loki',
                                            tagline='Glorious Purpose, King',
                                            year=2021)
        self.movie_2 = Movie.objects.create(title='Hawkeye',
                                            tagline='Holiday season, the best gifts are decorated with a bow',
                                            year=2021)
        self.movie_3 = Movie.objects.create(title='Marvel One-Shot: All Hail the King',
                                            tagline='All Hail the King',
                                            year=2014)

    def test_01_like(self):
        url = reverse('usermovierelation-detail', args=(self.movie_1.id,))

        data = {
            "like": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserMovieRelation.objects.get(user=self.user,
                                                 movie=self.movie_1)
        self.assertTrue(relation.like)

    def test_02_in_bookmarks(self):
        url = reverse('usermovierelation-detail', args=(self.movie_1.id,))
        data = {
            "in_bookmarks": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserMovieRelation.objects.get(user=self.user,
                                                 movie=self.movie_1)
        self.assertTrue(relation.in_bookmarks)

    def test_03_rate(self):
        url = reverse('usermovierelation-detail', args=(self.movie_1.id,))

        data = {
            "rate": 3,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserMovieRelation.objects.get(user=self.user,
                                                 movie=self.movie_1)
        self.assertEqual(3, relation.rate)

    def test_04_rate_wrong(self):
        url = reverse('usermovierelation-detail', args=(self.movie_1.id,))

        data = {
            "rate": 6,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)
