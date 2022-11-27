from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from recipes.models import Tag, Ingredient, Recipe
from users.models import Follow

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


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time')
