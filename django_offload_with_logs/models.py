# django_offload_with_logs/models.py
import uuid
from django.db import models

class OffloadTask(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_RUNNING = 'RUNNING'
    STATUS_SUCCESS = 'SUCCESS'
    STATUS_FAILURE = 'FAILURE'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    success_message = models.CharField(max_length=200, null=True, blank=True)
    fail_message = models.CharField(max_length=200, null=True, blank=True)
    message_duration = models.IntegerField(null=True, blank=True, help_text="Duration in ms")

    def mark_running(self):
        self.status = self.STATUS_RUNNING
        self.save(update_fields=['status', 'updated_at'])

    def mark_success(self):
        self.status = self.STATUS_SUCCESS
        self.save(update_fields=['status', 'updated_at'])

    def mark_failure(self):
        self.status = self.STATUS_FAILURE
        self.save(update_fields=['status', 'updated_at'])

    def __str__(self):
        return f"OffloadTask {self.id} [{self.status}]"