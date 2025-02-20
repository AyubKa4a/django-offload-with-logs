# django_offload_with_logs/views.py

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import OffloadTask

def task_status_view(request, task_id):
    try:
        task = OffloadTask.objects.get(pk=task_id)
        return JsonResponse({
            "status": task.status,
            "success_message": task.success_message,
            "fail_message": task.fail_message,
            "message_duration": task.message_duration,
            "toast_position": task.toast_position,
            "color_code": task.color_code,
        })
    except OffloadTask.DoesNotExist:
        return JsonResponse({"status": "NOT_FOUND"}, status=404)

@require_POST
def clear_tasks_view(request):
    data = json.loads(request.body.decode('utf-8') or '{}')
    new_task_ids = data.get('task_ids', [])
    request.session['offload_task_ids'] = new_task_ids
    return JsonResponse({"status": "updated", "task_ids": new_task_ids})
