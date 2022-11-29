from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django_filters import rest_framework as filters
from rest_framework import generics, views, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Follow

from .filters import FilterRecipe, IngredientSearchFilter
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCreateUpdateSerializer, RecipeListSerializer,
                          ShoppingCartSerializer,
                          SubscribeCreateDestroySerializer,
                          SubscribeListSerializer, TagSerializer)
from .utils import delete_object, post_object

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
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FilterRecipe
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeListSerializer
        else:
            return RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SubscribeListView(generics.ListAPIView):

    def get(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeListSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class SubscribeCreateDestroyView(views.APIView):

    def post(self, request, id):
        return post_object(SubscribeCreateDestroySerializer, request, id)

    def delete(self, request, id):
        return delete_object(User, Follow, request, id)


class FavoriteView(views.APIView):

    def post(self, request, id):
        return post_object(FavoriteSerializer, request, id)

    def delete(self, request, id):
        return delete_object(Recipe, Favorite, request, id)


class ShoppingCartView(views.APIView):

    def post(self, request, id):
        return post_object(ShoppingCartSerializer, request, id)

    def delete(self, request, id):
        return delete_object(Recipe, ShoppingCart, request, id)


class ShoppingCartDownloadView(views.APIView):

    @permission_classes([IsAuthenticated])
    def get(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(sum=Sum('amount'))
        shopping_list = "Список покупок:"
        for ingredient in ingredients:
            shopping_list += (
                f"\n{ingredient['ingredient__name']} "
                f"({ingredient['ingredient__measurement_unit']}) - "
                f"{ingredient['sum']}")
        file = 'shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file}.txt"'
        return response
