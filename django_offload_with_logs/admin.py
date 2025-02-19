# django_offload_with_logs/admin.py

from django.contrib import admin
from .models import OffloadTask

@admin.register(OffloadTask)
class OffloadTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
