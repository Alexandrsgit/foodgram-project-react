from django.contrib import admin

from recipes.models import Tag, Recipe, Ingredient, RecipeIngredient, User


class RecipeIngredientLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    list_display = (
        'name', 'measurement_units')
    list_filter = ('name')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = (RecipeIngredientLine, )

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')
