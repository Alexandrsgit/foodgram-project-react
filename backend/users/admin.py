from django.contrib import admin
from users.models import User, Subscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка пользователя."""

    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    empty_value_display = '-пусто-'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Админка подписки на автора."""

    list_display = ('id', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = '-пусто-'
