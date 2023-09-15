from django.contrib import admin
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)


class RecipeIngredientLine(admin.TabularInline):
    """Добавление поля ингредиентов в рецепты."""

    model = RecipeIngredient
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка тегов."""

    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка рецептов."""

    list_display = (
        'id', 'author', 'name', 'in_favorite')
    search_fields = ('author', 'name')
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientLine, )
    empty_value_display = '-пусто-'

    def in_favorite(self, obj):
        return obj.favorite.all().count()

    in_favorite.short_description = 'Колличество добавлений в избранное'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов."""

    list_display = (
        'name', 'measurement_units')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов для рецептов."""

    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_filter = ('recipe', 'ingredient')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Админка избранного."""

    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админка карзины покупок."""

    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    empty_value_display = '-пусто-'
