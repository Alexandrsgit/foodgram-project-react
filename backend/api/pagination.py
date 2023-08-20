from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    """Кастомный класс пагинации для users/."""

    page_size = 6
