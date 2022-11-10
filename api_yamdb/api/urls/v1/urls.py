from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ...views import (CategoryViewset, CommentViewSet, GenreViewset,
                      GetTokenView, ReviewViewSet, SignUpViewSet, TitleViewset,
                      UserViewSet)

app_name = 'api'

router = DefaultRouter()

router.register(r'categories', CategoryViewset)
router.register(r'genres', GenreViewset)
router.register(r'titles', TitleViewset, basename='titles')
router.register(
    r'titles/(?P<title>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title>\d+)/reviews/(?P<review>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register('auth/signup', SignUpViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', GetTokenView.as_view(), name='get_token'),
]
