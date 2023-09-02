from django.contrib import admin
from recipes.models import Tag, Recipe, Ingredient, RecipeIngredient


class RecipeIngredientLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientLine, )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'measurement_units')
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    pass
