from rest_framework import serializers
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Выбрано недопустимое имя.')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'role', 'bio')
