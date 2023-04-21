from rest_framework.serializers import ModelSerializer

from movie.models import Movie, UserMovieRelation


class MoviesSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class UserMovieRelationSerializer(ModelSerializer):
    class Meta:
        model = UserMovieRelation
        fields = ('movie', 'like', 'in_bookmarks', 'rate')