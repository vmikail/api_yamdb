from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .filters import TitleFilter
from .permissions import (IsAdministrator, IsAdminOrReadOnly,
                          IsOwnerOrReadOnlyFull, IsReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignUpSerializer,
                          TitleSerializer, TitleShowSerializer, UserSerializer)


class ListCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class SignUpViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    lookup_field = 'username'

    def create(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(username=username, email=email)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтрвеждения',
            message=f'Код подтверждения {confirmation_code} '
                    f'для пользователя {user.username}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[f'{user.email}'],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(views.APIView):
    def post(self, request):
        username = request.data.get('username', [])
        if not username:
            return Response(
                {'field_name': ['username']},
                status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=username)
        confirmation_code = request.data.get('confirmation_code', [])
        if default_token_generator.check_token(user, confirmation_code):
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response({'field_name': ['confirmation_code']},
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    permission_classes = (IsAdministrator,)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = self.get_serializer(request.user)
        if 'role' in request.data:
            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(Avg('review__score')).order_by('name')
    serializer_class = TitleShowSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleShowSerializer
        return TitleSerializer


class CategoryViewset(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (IsReadOnly(),)
        return super().get_permissions()


class GenreViewset(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (IsReadOnly(),)
        return super().get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerOrReadOnlyFull,)

    def get_queryset(self):
        title = self.kwargs.get('title')
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title'))
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsOwnerOrReadOnlyFull,)

    def get_queryset(self):
        title = self.kwargs.get('title')
        review = self.kwargs.get('review')
        return Comments.objects.filter(review=review, title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title'))
        review = get_object_or_404(Review, pk=self.kwargs.get('review'))
        serializer.save(
            title=title, review=review, author=self.request.user
        )
