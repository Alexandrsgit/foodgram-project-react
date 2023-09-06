from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from api.permissions import IsAdmin, IsUser
from rest_framework.response import Response
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from recipes.models import Tag, Recipe, Ingredient
from users.models import User, Subscription
from api.serializers import (
    TagSerializer, RecipeSerializer, RecipeCreateSerializer,
    IngredientSerializer)
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


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer