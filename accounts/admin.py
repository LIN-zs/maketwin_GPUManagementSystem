from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('额外信息', {'fields': ('role', 'max_concurrent_reservations', 'sudo_enabled')}),
    )
    list_display = ('username', 'email', 'role', 'sudo_enabled', 'is_staff')
    list_filter = ('role', 'sudo_enabled', 'is_staff')

admin.site.register(User, CustomUserAdmin)