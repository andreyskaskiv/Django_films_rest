from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from movie.models import Movie, UserMovieRelation
from movie.permissions import IsStaffOrReadOnly
from movie.serializers import MoviesSerializer, UserMovieRelationSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MoviesSerializer

    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['year', ]
    search_fields = ['title', 'tagline', ]
    ordering_fields = ['year', ]


class UserMoviesRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserMovieRelation.objects.all()
    serializer_class = UserMovieRelationSerializer
    lookup_field = 'movie'

    def get_object(self):
        obj, created = UserMovieRelation.objects.get_or_create(user=self.request.user,
                                                               movie_id=self.kwargs['movie'])
        # print('create', created)
        return obj
