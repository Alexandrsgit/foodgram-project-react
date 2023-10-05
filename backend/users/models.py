from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


# Список ролей пользователя
USER_ROLES = (
    ('user', 'Пользователь'),
    ('admin', 'Администратор'),
)


def validate_username(value):
    """Проверка имени пользователя."""
    invalid_usernames = ['me', 'set_password',
                         'subscriptions', 'subscribe']
    if value.lower() in invalid_usernames:
        raise ValidationError(
            'Недопустимое имя пользователя!'
        )
    return value


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(verbose_name='Логин', max_length=150,
                                unique=True,
                                validators=(UnicodeUsernameValidator(),
                                            validate_username,)
                                )
    first_name = models.CharField(verbose_name='Имя', max_length=150,)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150,)
    email = models.EmailField(verbose_name='Email', unique=True, blank=False,
                              null=False)
    role = models.CharField(verbose_name='Роль', max_length=20,
                            choices=USER_ROLES, default='user')
    password = models.CharField(max_length=150, verbose_name='Пароль')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']

    class Meta:
        """Уникальность полей в модели User."""

        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]

    @property
    def is_user(self):
        """User permission."""
        return self.is_user

    @property
    def is_admin(self):
        """Admin permission."""
        return self.is_admin

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписки на автора."""

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower', null=True,
                             verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following', null=True,
                               verbose_name='Избранный автор')

    class Meta:
        """Уникальность подписки."""

        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            )
        ]

    def __str__(self):
        return f'{self.user.username} подписан на {self.author.username}'
