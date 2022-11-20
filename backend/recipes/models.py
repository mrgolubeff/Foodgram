from django.db import models

from users.models import User


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(
        User
    )
    image = models.ImageField()
    cooking_time = models.IntegerField() #Добавить минимальное значение


class Tag(models.Model):
    pass


class Ingredient(models.Model):
    pass
