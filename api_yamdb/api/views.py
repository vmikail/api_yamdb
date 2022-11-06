from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import mixins, viewsets, status, views
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdministrator
from .serializers import SignUpSerializer, UserSerializer

from users.models import User


class SignUpViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    lookup_field = 'username'

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        username = data.get('username')
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтрвеждения',
            message=f'Код подтверждения {confirmation_code} '
                    f'для пользователя {user.username}',
            from_email='admin@yamdb.ru',
            recipient_list=[f'{user.email}'],
            fail_silently=False
        )
        return Response(data, status=status.HTTP_200_OK)


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
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        return Response({"field_name": ['confirmation_code']},
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
        serializer = UserSerializer(request.user)
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
