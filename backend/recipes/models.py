from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Tag(models.Model):
    """Модель Тега."""

    name = models.CharField(max_length=200, verbose_name='Название',
                            help_text='Введите название тега',
                            unique=True)
    color = models.CharField(max_length=7, verbose_name='Цвет',
                             help_text='Введите цвет в HEX',
                             unique=True)
    slug = models.CharField(max_length=200, verbose_name='slug',
                            help_text='Укажите уникальный слаг',
                            unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""

    tags = models.ManyToManyField(Tag, verbose_name='Название тега',
                                  help_text='Выбирите тег')
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
        blank=True,
        help_text='Добавьте изображение готового блюда'
    )
    name = models.CharField(max_length=200, verbose_name='Название пецепта',
                            help_text='Введите навзание рецепта')
    cooking_time = models.PositiveIntegerField(validators=[
        MinValueValidator(
            1, 'Время приготовления не должно быть меньше 1 минуты')],
        verbose_name='Время приготовления')
    text = models.TextField(verbose_name='Описание рецепта',
                            help_text='Введите описание рецепта')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор')
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиент'
    )

    class Meta:
        """Проверка уникальности рецепта."""

        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='unique_recipe')]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(max_length=200, verbose_name='Название',
                            help_text='Введите название ингредиента')
    measurement_units = models.CharField(max_length=200,
                                         verbose_name='Единицы измерения',
                                         help_text='Введите единицу измерения')

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель для связи Рецепта и Ингредиентов."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredients',
                               verbose_name='Название рецепта',
                               help_text='Выберите рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='Ингредиент',
                                   help_text='Укажите ингредиенты')
    amount = models.PositiveIntegerField(validators=[
        MinValueValidator(
            1, 'Время приготовления не должно быть меньше 1 минуты')],
        verbose_name='Время приготовления',
        help_text='Укажите количество ингредиента')

    class Meta:
        """Проверка на уникальность рецепта."""

        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredients')]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class Favorite(models.Model):
    """Модель избранного."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorite',
                               verbose_name='Рецепт')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorite',
                             verbose_name='Пользователь')

    class Meta:
        """Проверка уникальности избранного."""

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в избраннное'


class ShoppingCart(models.Model):
    """Модель списка покупок."""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='shopping_cart',
                               verbose_name='Рецепт для приготовления',
                               help_text='Выберите рецепт для приготовления')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shopping_cart',
                             verbose_name='Пользователь')

    class Meta:
        """Уникальность полей списка покупок."""

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_cart'
            )
        ]

    def __str__(self):
        return (f'{self.user.username} добавил'
                f'{self.recipe.name} в список покупок')
