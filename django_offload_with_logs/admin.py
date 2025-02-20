# django_offload_with_logs/admin.py

from django.contrib import admin
from .models import OffloadTask

@admin.register(OffloadTask)
class OffloadTaskAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'status', 'user', 'created_at', 'updated_at',
        'toast_position', 'color_code', 'duration_ms'
    )
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at', 'start_time', 'end_time', 'user')

    fieldsets = (
        (None, {
            'fields': ('id', 'status', 'user', 'created_at', 'updated_at')
        }),
        ("Timing", {
            'fields': ('start_time', 'end_time'),
        }),
        ("Messages", {
            'fields': ('success_message', 'fail_message', 'message_duration'),
        }),
        ("UI Options", {
            'fields': ('toast_position', 'color_code'),
        }),
    )
