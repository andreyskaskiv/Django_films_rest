from django.contrib import admin
from django.contrib.admin import ModelAdmin

from movie.models import Movie


@admin.register(Movie)
class MovieAdmin(ModelAdmin):
    """How and what will be reflected in the admin panel"""

    list_display = ('title', 'year',)
    fields = ('title', 'tagline', 'description', 'year')
    list_filter = ('year',)
    search_fields = ('year',)
    ordering = ('-year',)
