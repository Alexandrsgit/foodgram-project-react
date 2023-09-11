from api.permissions import IsAdmin, IsUser
from api.serializers import (IngredientSerializer, FavoriteSerializer,
                             RecipeSerializer, TagSerializer,
                             RecipeCrudSerializer,
                             UserSubscribeSerializer,
                             UserSubscribeRepresentSerializer)
from django.shortcuts import HttpResponse, get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from users.models import User, Subscription


class UserSubscribeView(APIView):
    """Подписка/отписка от пользователя."""

    def post(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        serializer = UserSubscribeSerializer(
            data={'subscriber': request.user.id, 'author': author.id},
            context={'requser': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, requset, user_id):
        author = get_object_or_404(User, id=user_id)
        if not Subscription.objects.filter(subscriber=requset.user,
                                           author=author).exists():
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscription.objects.get(subscriber=requset.user,
                                 author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSubscriptionViewSet(mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    """Все подписки на пользователя."""

    serializer_class = UserSubscribeRepresentSerializer

    def get_queryset(self):
        return User.objects.filter(following_author=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для Тега."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для Инргедиента."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    """Вьюсет для Рецепта."""

    queryset = Recipe.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer(self):
        if self.action in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCrudSerializer

    @action(
        detail=True,
        method=['post', 'delete'],
        permision_classes=[IsAuthenticated, ]
    )
    def favorite(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
            if Favorite.objects.filter(user=user,
                                       recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже был добавлен.'},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = FavoriteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if not Favorite.objects.filter(user=user,
                                       recipe=recipe).exists():
            return Response({'errors': 'Рецепт не найден'},
                            status=status.HTTP_404_NOT_FOUND)
        Favorite.objects.get(recipe=recipe).delete()
        return Response('Рецепт удалён из избранного',
                        status=status.HTTP_204_NO_CONTENT)
    
    @action(
        detail=True,
        methods=['post', 'delete'],
        permision_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        user = self.request.user
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user,
                                           recipe=recipe).exists():
                return Response({'error': ''})