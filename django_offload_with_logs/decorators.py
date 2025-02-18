# django_offload_with_logs/decorators.py
from django.conf import settings
from .store import function_queue
from .models import OffloadTask

OFFLOAD_IMMEDIATE = getattr(settings, 'OFFLOAD_IMMEDIATE', False)

def enable(func):
    """
    Decorator that adds <func>.offload(*args, **kwargs).
    Offloads the func to run after the response is returned.
    Returns a task_id string (UUID).
    """
    def offload(*args, **kwargs):
        if OFFLOAD_IMMEDIATE:
            func(*args, **kwargs)
            return None

        success_message = kwargs.pop('success_message', None)
        fail_message = kwargs.pop('fail_message', None)
        message_duration = kwargs.pop('message_duration', None)

        task = OffloadTask.objects.create(
            status=OffloadTask.STATUS_PENDING,
            success_message=success_message,
            fail_message=fail_message,
            message_duration=message_duration
        )

        function_queue.append((func, args, kwargs, str(task.id)))

        if args and hasattr(args[0], 'META'):
            request = args[0]
            if hasattr(request, '_offload_task_ids'):
                request._offload_task_ids.append(str(task.id))

        return str(task.id)

    func.offload = offload
    return func