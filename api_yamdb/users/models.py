from django.db import models
from django.contrib.auth.models import AbstractUser

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
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ['username', ]

    def __str__(self):
        return self.username
