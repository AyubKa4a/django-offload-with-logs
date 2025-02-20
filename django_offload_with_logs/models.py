# django_offload_with_logs/models.py

import uuid
import datetime
from django.db import models
from django.conf import settings

class OffloadTask(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_RUNNING = 'RUNNING'
    STATUS_SUCCESS = 'SUCCESS'
    STATUS_FAILURE = 'FAILURE'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Basic message fields
    success_message = models.CharField(max_length=200, null=True, blank=True)
    fail_message = models.CharField(max_length=200, null=True, blank=True)
    message_duration = models.IntegerField(null=True, blank=True, help_text="Toast duration in ms")

    # Additional fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="User who triggered"
    )
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    # UI preferences for the toast
    toast_position = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Where to show toast (e.g. 'top-right', 'bottom-left')"
    )
    color_code = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        help_text="Hex color code for toast background, e.g. #FF0000"
    )

    def mark_running(self):
        self.status = self.STATUS_RUNNING
        self.start_time = datetime.datetime.now()
        self.save(update_fields=['status', 'start_time', 'updated_at'])

    def mark_success(self):
        self.status = self.STATUS_SUCCESS
        self.end_time = datetime.datetime.now()
        self.save(update_fields=['status', 'end_time', 'updated_at'])

    def mark_failure(self):
        self.status = self.STATUS_FAILURE
        self.end_time = datetime.datetime.now()
        self.save(update_fields=['status', 'end_time', 'updated_at'])

    def duration_ms(self):
        """
        Returns how long the task took in milliseconds, or None if not finished.
        """
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() * 1000)
        return None

    def __str__(self):
        return f"OffloadTask {self.id} [{self.status}]"
