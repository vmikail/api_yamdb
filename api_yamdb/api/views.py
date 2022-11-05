from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Comments, Genre, Reviews, Title

from .filters import TitleFilter
from .permissions import IsReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewsSerializer, TitleSerializer,
                          TitleShowSerializer)


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        Avg("reviews__score")
    )
    serializer_class = TitleShowSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleShowSerializer
        return TitleSerializer

    # def get_queryset(self):
    #     return Title.objects.all().annotate(arating=Avg('reviews__score'))


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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        title = self.kwargs.get('title') 
        return Reviews.objects.filter(title=title)

    def perform_update(self, serializer): 
        if ((serializer.instance.author != self.request.user)
            or (not self.request.user.is_admin)
            or (not self.request.user.is_moderator)
            or (not self.request.user.is_superuser)
        ):
            raise PermissionDenied('У вас нет прав на изменение контента!')
        super(ReviewViewSet, self).perform_update(serializer) 
    
    def perform_destroy(self, instance): 
        if ((instance.author != self.request.user)
            or (not self.request.user.is_admin)
            or (not self.request.user.is_moderator)
            or (not self.request.user.is_superuser)
        ):
            raise PermissionDenied('У вас нет прав на удаление контента!')
        instance.delete() 


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        review = self.kwargs.get('review')
        return Comments.objects.filter(review=review)

    def perform_update(self, serializer):
        if ((serializer.instance.author != self.request.user)
            or (not self.request.user.is_admin)
            or (not self.request.user.is_moderator)
            or (not self.request.user.is_superuser)):
            raise PermissionDenied('У вас нет прав на изменение контента!')
        super(ReviewViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if ((instance.author != self.request.user)
            or (not self.request.user.is_admin)
            or (not self.request.user.is_moderator)
            or (not self.request.user.is_superuser)):
            raise PermissionDenied('У вас нет прав на удаление контента!')
        instance.delete()
