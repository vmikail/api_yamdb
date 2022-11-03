from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CategoryViewset, GenreViewset, TitleViewset

router = DefaultRouter()

router.register(r'categories', CategoryViewset)
router.register(r'genres', GenreViewset)
router.register(r'titles', TitleViewset)

urlpatterns = [
    path('v1/', include(router.urls))
]
