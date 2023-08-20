from rest_framework import permissions


class IsModerOrAdminOrAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)


class IsUser(permissions.BasePermission):
    """Кастомный класс для проверки прав для роли user."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'user'
                     or request.user.role == 'admin'
                     or request.user.role == 'moderator'))

    def has_object_permission(self, request, view, obj):
        """Функция проверяет является ли пользователь user."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and obj.author == request.user
                and (request.user.role == 'user'
                     or request.user.role == 'admin'
                     or request.user.role == 'moderator'))


class IsModeraror(permissions.BasePermission):
    """Кастомный класс для проверки прав для роли moderator."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == 'moderator')

    def has_object_permission(self, request, view, obj):
        """Функция проверяет является ли пользователь moderator."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.role == 'moderator')


class IsAdmin(permissions.BasePermission):
    """Кастомный класс для проверки прав для роли admin."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser is True)

    def has_object_permission(self, request, view, obj):
        """Функция проверяет является ли пользователь admin."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser is True)
