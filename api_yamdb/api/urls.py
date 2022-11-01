from django.urls import include, path
from rest_framework import routers

from .views import SignUpViewSet


app_name = 'api'

router = routers.DefaultRouter()
router.register('auth/signup', SignUpViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
