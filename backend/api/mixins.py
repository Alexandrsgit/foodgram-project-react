from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.pagination import UserPagination
from api.permissions import IsAdmin


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Mixins для GET, POST, DELETE запросов."""

    permission_classes = (IsAdmin,)
    lookup_field = 'slug'
    pagination_class = UserPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)

    def get_permissions(self):
        """Выбираем permissions с правами доступа
        в зависимости от метода запроса."""
        if self.request.method == 'GET':
            return (IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()
