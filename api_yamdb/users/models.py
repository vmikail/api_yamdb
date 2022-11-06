from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLES = (
    (USER, 'Пользователь'),
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор')
)


class User(AbstractUser):
    email = models.EmailField('Электронная почта', unique=True)
    role = models.CharField('Роль пользователя',
                            max_length=10,
                            choices=ROLES,
                            default=USER)
    bio = models.TextField('Биография',
                           blank=True,
                           null=True)
    password = models.CharField('Пароль',
                                max_length=128,
                                blank=True,
                                null=True,
                                default='')

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username
