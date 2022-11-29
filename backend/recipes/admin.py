from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient, RecipeTag,
                     Tag)

EMPTY = '-пусто-'


class IngredientInline(admin.StackedInline):

    model = RecipeIngredient


class TagInline(admin.StackedInline):

    model = RecipeTag


class RecipeAdmin(admin.ModelAdmin):

    list_display = [
        'name',
        'cooking_time',
        'favorites',
        'author'
    ]
    search_fields = ['name']
    list_filter = ['tags', 'author__username']
    empty_value_display = EMPTY
    inlines = [IngredientInline, TagInline]

    def favorites(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


class IngredientAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'measurement_unit']
    search_fields = ['name']
    empty_value_display = EMPTY


class TagAdmin(admin.ModelAdmin):

    list_display = ('name', 'color', 'slug')
    search_fields = ['name']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
