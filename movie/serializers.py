from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from movie.models import Movie, UserMovieRelation


class MovieReaderSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class MoviesSerializer(ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    readers = MovieReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'description', 'year', 'readers',
                  'annotated_likes', 'rating')


class UserMovieRelationSerializer(ModelSerializer):
    class Meta:
        model = UserMovieRelation
        fields = ('movie', 'like', 'in_bookmarks', 'rate')
