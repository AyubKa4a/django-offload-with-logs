# django_offload_with_logs/urls.py
from django.urls import path
from .views import task_status_view, clear_tasks_view

urlpatterns = [
    path('task-status/<uuid:task_id>/', task_status_view, name='offload_status'),
    path('clear-tasks/', clear_tasks_view, name='offload_clear_tasks'),
]