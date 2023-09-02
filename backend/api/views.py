from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from api.permissions import IsAdmin, IsUser
from rest_framework.response import Response
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from recipes.models import Tag, Recipe, User, Follow, Favorite, ShoppingCart
from api.serializers import (
    TagSerializer, RecipeSerializer, RecipeCreateSerializer, UserSerializer,
    FollowSerializer,
    FavoriteSerializer, ShoppingCartSerializer)
from rest_framework.permissions import AllowAny



class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
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


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsUser,)
#    filter_backends = (filters.SearchFilter,)
#    search_fields = ('=user__username', '=following__username')

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class ShoppingCartViewSet(ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
