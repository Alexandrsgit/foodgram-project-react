from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')
    empty_value_display = '-пусто-'
