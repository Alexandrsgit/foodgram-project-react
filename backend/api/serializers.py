from rest_framework import serializers
from recipes.models import USER_ROLES, Tag, Recipe, RecipeIngredient, Ingredient, User, Follow, Favorite, ShoppingCart
from rest_framework.validators import UniqueTogetherValidator
from djoser.serializers import UserCreateSerializer, UserSerializer

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fileds = '__all__'


class UserSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')

#    def validate(self, obj):
#        invalid_usernames = ['me', 'set_password',
#                             'subscriptions', 'subscribe']
#        if self.initial_data.get('username') in invalid_usernames:
#            raise serializers.ValidationError(
#                {'username': 'Вы не можете использовать этот username.'}
#            )
#        return obj


class UserGetSerializer(UserSerializer):
    """Сериализатор для работы с информацией о пользователях."""
    # is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

#    def get_is_subscribed(self, obj):
#        request = self.context.get('request')
#        return (request.user.is_authenticated
#                and Subscription.objects.filter(
#                    user=request.user, author=obj
#                ).exists())

#    def get_is_subscribed(self, obj):
#        return (
#            self.context.get('request').user.is_authenticated
#            and Subscribe.objects.filter(user=self.context['request'].user,
#                                         author=obj).exists()
#        )



class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('__all__')
        # Проверка UniqueConstraint на уровне сериализатора.
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate(self, data):
        """Проверка чтобы нельзя было подписаться на себя."""
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError('Нельзя подписаться на себя!')
        return data


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_units = serializers.CharField(
        source='ingredient.measurement_units')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_units', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    # ingredients = RecipeIngredientSerializer(many=True, source='recipeingredient_set')
    ingredients = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')

    def get_ingredients(self, instance):
        return RecipeIngredientSerializer(
            instance.recipeingredient_set.all(),
            many=True
        ).data


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientCreateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time', 'text', 'tags', 'ingredients')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)

        for ingredient_data in ingredients:
            RecipeIngredient(
                recipe=instance,
                ingredient=ingredient_data['ingredient'],
                amount=ingredient_data['amount']
            ).save()
        return instance
    
#    def to_representation(self, instance):
#        return super().to_representation(instance)
    

