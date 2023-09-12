from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# Список ролей пользователя
USER_ROLES = (
    ('user', 'Пользователь'),
    ('admin', 'Администратор'),
)


def validate_username(value):
    invalid_usernames = ['me', 'set_password',
                         'subscriptions', 'subscribe']
    if value.lower() in invalid_usernames:
        raise ValidationError(
            'Недопустимое имя пользователя!'
        )
    return value


class User(AbstractUser):
    """Модель пользователя."""

    role = models.CharField(max_length=20, verbose_name='Роль',
                            choices=USER_ROLES, default='user')

    class Meta:
        """Уникальность полей в модели User."""

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

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            )
        ]

    def __str__(self):
        """Кто на кого подписан."""
        return f'{self.user.username} подписан на {self.author.username}'
