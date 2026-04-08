from django.contrib import admin
from .models import GPU, Reservation

@admin.register(GPU)
class GPUAdmin(admin.ModelAdmin):
    list_display = ('gpu_index', 'name', 'status')
    list_filter = ('status',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'gpu', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'gpu')
    search_fields = ('user__username',)