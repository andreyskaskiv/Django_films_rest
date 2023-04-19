from rest_framework.viewsets import ModelViewSet

from movie.models import Movie
from movie.serializers import MoviesSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MoviesSerializer
