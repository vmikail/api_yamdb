from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from .serializers import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre, Title
from .serializers import TitleSerialiser


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerialiser
    pagination_class = PageNumberPagination


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewset(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
