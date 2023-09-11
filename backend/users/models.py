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
    is_subscribed = models.BooleanField(default=False)

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

    subscriber = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='subscriber', null=True,
                                   verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following_author', null=True,
                               verbose_name='Избранный автор')

    class Meta:
        """Уникальность подписки."""

        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'],
                name='unique_subscriber'
            )
        ]

    def __str__(self):
        """Кто на кого подписан."""
        return f'{self.subscriber.username} подписан на {self.author.username}'
