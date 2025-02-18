# django_offload_with_logs/admin.py

from django.contrib import admin
from .models import AfterResponseTask

@admin.register(AfterResponseTask)
class AfterResponseTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
