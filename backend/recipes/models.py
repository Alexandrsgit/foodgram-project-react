from django.db import models
from users.models import User


class Tag(models.Model):
    """Модель Тэга."""

    name = models.CharField(max_length=200, verbose_name='Название')
    color = models.CharField(max_length=7, verbose_name='Цвет')
    slug = models.CharField(max_length=200, verbose_name='slug', unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""

    tags = models.ManyToManyField(Tag)
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
        blank=True,
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    cooking_time = models.PositiveIntegerField(verbose_name='Время приготовления')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    is_in_shopping_cart = models.BooleanField(default=False, verbose_name='В корзине')
    is_favorited = models.BooleanField(default=False, verbose_name='В избранном')
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient')
    )
    count = models.IntegerField(verbose_name='Колличество добавлений рецепта', default=0)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    measurement_units = models.CharField(max_length=200, verbose_name='Единицы измерения')

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name='Количество')


class Follow(models.Model):
    """Модель подписки на автора."""

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower', null=True,
                             verbose_name='Пользователь',
                             help_text='Укажите пользователя')
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='following', null=True,
                                  verbose_name='Избранный автор',
                                  help_text='Укажите автора рецепта')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follower'
            )
        ]


class Favorite(models.Model):
    """Модель избранного."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ShoppingCart(models.Model):
    """Модель списка покупок."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    download = models.BooleanField(default=False, verbose_name='Скачать')

