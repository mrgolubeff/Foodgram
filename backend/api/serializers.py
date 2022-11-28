from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Tag, Ingredient, Recipe, RecipeIngredient, RecipeTag)
from users.models import Follow
from recipes.models import Favorite, ShoppingCart
from .utils import Base64ImageField

User = get_user_model()


class CustomUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed'
        )
    
    def get_is_subscribed(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if isinstance(user, AnonymousUser) or not user:
            return False
        subscription_exists = Follow.objects.filter(
            user=user,
            author=obj
        ).exists()
        return subscription_exists


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):

    tags = TagSerializer(read_only=True, many=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        data = RecipeIngredientSerializer(ingredients, many=True).data
        return data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, recipe=obj
        ).exists()
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj
        ).exists()


class RecipeMiniSerializer(serializers.ModelSerializer):

    class Meta:

        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class AddingIngredientSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()

    class Meta:

        model = RecipeIngredient
        fields = ['id', 'amount']


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):

    ingredients = AddingIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField(required=True, allow_null=False)

    class Meta:

        model = Recipe
        fields = (
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        read_only_fields = ('author',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient['amount']
            )
        for tag in tags:
            RecipeTag.objects.create(recipe=recipe, tag=tag)
        return recipe

    def update(self, instance, validated_data):
        RecipeTag.objects.filter(recipe=instance).delete()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.image = validated_data.get('image')
        instance.cooking_time = validated_data.get('cooking_time')
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=instance,
                amount=ingredient['amount']
            )
        for tag in tags:
            RecipeTag.objects.create(recipe=instance, tag=tag)
        instance.save()
        return instance

    def to_representation(self, recipe):
        return RecipeListSerializer(recipe, context=self.context).data

########### !!!

class SubscribeListSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:

        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context['request']
        if Follow.objects.filter(user=request.user, author=obj).exists():
            return True
        return False

    def get_recipes(self, obj):
        request = self.context['request']
        if request.user.is_anonymous:
            return False
        recipes = Recipe.objects.filter(author=obj)
        limit = request.query_params['recipes_limit']
        if limit:
            recipes = recipes[:int(limit)]
        return RecipeListSerializer(
            recipes, many=True, context=self.context).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class SubscribeCreateDestroySerializer(serializers.ModelSerializer):

    class Meta:

        model = Follow
        fields = (
            'user',
            'author'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author'],
                message='Подписка уже существует!'
            )
        ]

    def validate_author(self, value):
        request = self.context['request']
        if value == request.user:
            raise serializers.ValidationError(
                'Попытка подписки на самого себя'
            )
        return value

    def to_representation(self, instance):
        return SubscribeListSerializer(
                instance.author,
                context=self.context
            ).data


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:

        model = Favorite
        fields = ['user', 'recipe']

    def to_representation(self, instance):
        return RecipeMiniSerializer(
                instance.recipe,
                context=self.context
            ).data


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:

        model = ShoppingCart
        fields = ['user', 'recipe']
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['user', 'recipe'],
                message='Рецепт уже добавлен в список покупок'
            )
        ]

    def to_representation(self, instance):
        return RecipeMiniSerializer(
                instance.recipe,
                context=self.context
            ).data
