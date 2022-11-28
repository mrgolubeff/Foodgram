from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from .paginators import PaginationWithLimit
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly

from recipes.models import Tag, Ingredient, Recipe
from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeListSerializer,
    RecipeCreateUpdateSerializer
)
from .filters import IngredientSearchFilter


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
