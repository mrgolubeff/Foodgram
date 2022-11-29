from django.contrib import admin

from recipes.admin import EMPTY

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):

    list_display = ['id', 'username', 'email', 'first_name', 'last_name']
    search_fields = ['username', 'email']
    ordering = ['id']
    empty_value_display = EMPTY


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
