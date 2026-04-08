from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SudoRequest

@admin.register(SudoRequest)
class SudoRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'valid_until', 'created_at')
    list_filter = ('status',)