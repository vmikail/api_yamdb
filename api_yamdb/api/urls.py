from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewset, GenreViewset, TitleViewset

router = DefaultRouter()

router.register(r'category', CategoryViewset, basename='category')
router.register(r'genres', GenreViewset, basename='genre')
router.register(r'title', TitleViewset, basename='title')

urlpatterns = [
    path('v1/', include(router.urls))
]
