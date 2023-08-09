from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


class CustomUserAdmin(UserAdmin):
    search_fields = ['email', 'phone_number']


admin.site.register(User, CustomUserAdmin)
