from api.permissions import IsAdmin, IsUser
from api.serializers import (IngredientSerializer, RecipeSerializer,
                             RecipeCreateSerializer, TagSerializer)
from rest_framework.viewsets import ModelViewSet
from recipes.models import Ingredient, Recipe, Tag
from users.models import User, Subscription


class TagViewSet(ModelViewSet):
    """Вьюсет для Тега."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    """Вьюсет для Рецепта."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'recipeingredient_set__ingredient', 'tags'
        ).all()
        return recipes

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(ModelViewSet):
    """Вьюсет для Инргедиента."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
