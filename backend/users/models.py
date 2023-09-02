from django.db import models
from django.contrib.auth.models import AbstractUser


USER_ROLES = (
    ('user', 'Пользователь'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    """Модель пользователя."""

    role = models.CharField(max_length=20, verbose_name='Роль',
                            choices=USER_ROLES, default='user')
    is_subscribed = models.BooleanField(default=False)
    token = models.CharField(max_length=200,
                                  verbose_name='Токен авторизации',
                                  blank=True)

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

