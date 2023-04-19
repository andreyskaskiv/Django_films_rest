from rest_framework.serializers import ModelSerializer

from movie.models import Movie


class MoviesSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
