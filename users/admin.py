from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    search_fields = ['email', 'first_name', 'last_name', 'phone_number']
    ordering = ('-date_joined', )
    list_per_page = 25
    list_display = [
        'email', 'phone_number', 'first_name', 'last_name', 'gender']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'phone_number',)
        }),
        ('Permissions', {'fields': ('is_staff', 'user_permissions')}),
        ('Group Permissions', {'fields': ('groups', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
