from django.urls import include, path
from rest_framework import routers

from .views import GetTokenView, SignUpViewSet, UserViewSet


app_name = 'api'

router = routers.DefaultRouter()
router.register('auth/signup', SignUpViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', GetTokenView.as_view(), name='get_token'),

]
