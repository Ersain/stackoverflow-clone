from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = (
        'pk',
        'user__username'
    )
