from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteView, IngredientViewSet, RecipeViewSet,
                    ShoppingCartDownloadView, ShoppingCartView,
                    SubscribeCreateDestroyView, SubscribeListView, TagViewSet)

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('users/<int:id>/subscribe/',
         SubscribeCreateDestroyView.as_view()),
    path('users/subscriptions/',
         SubscribeListView.as_view(),
         name='subscriptions'),
    path('recipes/<int:id>/shopping_cart/',
         ShoppingCartView.as_view(),
         name='shopping_cart'),
    path('recipes/<int:id>/favorite/',
         FavoriteView.as_view(),
         name='favorite'),
    path('recipes/download_shopping_cart/',
         ShoppingCartDownloadView.as_view(),
         name='donwload_cart'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
