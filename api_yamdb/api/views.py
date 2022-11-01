from requests import Response

from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import mixins, viewsets, status

from .serializers import SignUpSerializer
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
            message=f'Код подтверждения {confirmation_code}',
            from_email='admin@yamdb.ru',
            recipient_list=[f'{user.email}'],
            fail_silently=False
        )
        return Response(data, status=status.HTTP_200_OK)
