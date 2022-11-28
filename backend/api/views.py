from django.shortcuts import render
from rest_framework import viewsets, generics, views
from rest_framework.pagination import LimitOffsetPagination
from .paginators import PaginationWithLimit
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly

from recipes.models import Tag, Ingredient, Recipe, Favorite, ShoppingCart
from users.models import Follow
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeListSerializer,
    RecipeCreateUpdateSerializer,
    SubscribeListSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
    SubscribeCreateDestroySerializer
)
from .filters import IngredientSearchFilter
from django.contrib.auth import get_user_model

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        else:
            return RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SubscribeListView(generics.ListAPIView):
    
    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)


class SubscribeListView(generics.ListAPIView):
    """Представление вывода подписок."""

    def get(self, request):
        """Метод получения списка подписок."""
        user = request.user
        queryset = User.objects.filter(follower__user=user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeListSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class SubscribeCreateDestroyView(views.APIView):
    """Представление создания подписок."""

    def post(self, request, id):
        """Метод создания подписки."""
        return post_object(SubscribeCreateDestroySerializer, request, id)

    def delete(self, request, id):
        """Метод удаления подписки."""
        return delete_object(User, Follow, request, id)


class FavoriteView(views.APIView):
    """Представление избранного."""

    def post(self, request, id):
        """Метод добавления рецепта в список избранного."""
        return post_object(FavoriteSerializer, request, id)

    def delete(self, request, id):
        """Метод удаления рецепта из списка избранного."""
        return delete_object(Recipe, Favorite, request, id)


class ShoppingCartView(views.APIView):
    """Представление списка покупок."""

    def post(self, request, id):
        """Метод добавления рецепта в список покупок."""
        return post_object(ShoppingCartSerializer, request, id)

    def delete(self, request, id):
        """Метод удаления рецепта из списка покупок."""
        return delete_object(Recipe, ShoppingCart, request, id)
