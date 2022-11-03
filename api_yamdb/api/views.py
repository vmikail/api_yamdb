from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from .serializers import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre, Title
from .serializers import TitleSerialiser
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilter


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerialiser
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewset(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)
