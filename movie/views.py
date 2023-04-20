from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from movie.models import Movie
from movie.permissions import IsStaffOrReadOnly
from movie.serializers import MoviesSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MoviesSerializer

    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['year', ]
    search_fields = ['title', 'tagline', ]
    ordering_fields = ['year', ]

