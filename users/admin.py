from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    search_fields = ['email', 'phone_number']
    ordering = ('-date_joined', )
    list_per_page = 25
    list_display = [
        'email', 'phone_number', 'first_name', 'last_name', 'gender']


admin.site.register(User, CustomUserAdmin)
