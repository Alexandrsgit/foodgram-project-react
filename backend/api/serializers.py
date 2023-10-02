from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import User, Subscription
from .utils import Base64ImageField, Hex2NameColor


class CustomUserSerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')


class UserGetSerializer(UserSerializer):
    """Сериализатор для работы с моделью User."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and Subscription.objects.filter(
                    user=request.user, author=obj
                ).exists())


class RecipeLightSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с краткой информацией о рецепте."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSubscribeRepresentSerializer(UserGetSerializer):
    """Информация о подписках пользователя."""

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'username', 'first_name', 'last_name',
                            'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.id)
        if limit and limit.isdigit():
            recipes = recipes[:int(limit)]
        return RecipeLightSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.id).count()


class UserSubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки/отписки от пользователей."""

    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author'),
                message='Вы уже подписаны на этого пользователя'
            )
        ]

    def validate(self, data):
        request = self.context.get('request')
        if request.user == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписываться на самого себя!'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return UserSubscribeRepresentSerializer(
            instance.author, context={'request': request}
        ).data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью Tag."""

    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью Ingredient."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью RecipeIngredient."""

    id = serializers.ReadOnlyField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_units = serializers.CharField(
        source='ingredient.measurement_units', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_units', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделью Recipe."""

    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True,
                                             source='recipe_ingredients')
    author = UserGetSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and Favorite.objects.filter(
                    user=request.user, recipe=obj
                ).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and ShoppingCart.objects.filter(
                    user=request.user, recipe=obj
                ).exists())


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания игредиента."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCrudSerializer(RecipeSerializer):
    """Сериализатор для модели Recipe(CRUD)."""

    id = serializers.ReadOnlyField()
    ingredients = RecipeIngredientCreateSerializer(
        many=True,
        write_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True)
    image = Base64ImageField()
    author = UserGetSerializer(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image', 'name', 'text',
                  'cooking_time', 'author')

    def validate(self, obj):
        for field in ['name', 'text', 'cooking_time']:
            if not obj.get(field):
                raise serializers.ValidationError(
                    f'{field} - Поле обазательно для заполнения.'
                )
        if not obj.get('tags'):
            raise serializers.ValidationError(
                'Необходимо указать хотя бы один тег!'
            )
        if not obj.get('ingredients'):
            raise serializers.ValidationError(
                'Необходимо указать хотя бы один ингредиент!'
            )
        inrgedient_id_list = [item['id'] for item in obj.get('ingredients')]
        unique_ingredient_id_list = set(inrgedient_id_list)
        if len(inrgedient_id_list) != len(unique_ingredient_id_list):
            raise serializers.ValidationError(
                'Выбранные ингредиенты должны быть уникальны.'
            )
        return obj

    def to_representation(self, instance):
        return RecipeSerializer(instance,
                                context=self.context).data

    def add_tags_ingredients(self, ingredients, tags, model):
        for ingredient in ingredients:
            RecipeIngredient.objects.update_or_create(
                recipe=model,
                ingredient=ingredient['id'],
                amount=ingredient['amount'])
        model.tags.set(tags)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        self.add_tags_ingredients(ingredients, tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        self.add_tags_ingredients(ingredients, tags, instance)
        return super().update(instance, validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Favorite."""

    name = serializers.ReadOnlyField(
        source='recipe.name',
        read_only=True)
    image = serializers.ImageField(
        source='recipe.image',
        read_only=True)
    coocking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='recipe',
        read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'coocking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ShoppingCart."""

    name = serializers.ReadOnlyField(
        source='recipe.name',
        read_only=True)
    image = serializers.ImageField(
        source='recipe.image',
        read_only=True)
    coocking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='recipe',
        read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'coocking_time')
