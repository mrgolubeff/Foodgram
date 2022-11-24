from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import TagViewSet, IngredientViewSet, RecipeViewSet

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]