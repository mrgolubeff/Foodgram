from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение рецепта'
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления'
    )
    tags = models.ManyToManyField(
        'Tag',
        through='RecipeTag',
        related_name='recipes',
        verbose_name='Теги рецепта'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Ингредиенты рецепта'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания рецепта'   
    )

    class Meta():

        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=40,
        unique=True,
        verbose_name='Название тега'
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет тега (HEX-код)'
    )
    slug = models.SlugField(
        max_length=40,
        unique=True,
        verbose_name='Жетон тега'
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=40,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=15,
        verbose_name='Единица измерения ингредиента'
    )

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0.1)])


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Подписавшийся'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited',
        verbose_name='Рецепт в избранном'
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]


class ShoppingCart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Добавивший в корзину'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт в корзине'
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart_recipe'
            )
        ]
