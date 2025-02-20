# django_offload_with_logs/decorators.py

from django.conf import settings
from .store import function_queue
from .models import OffloadTask

OFFLOAD_IMMEDIATE = getattr(settings, 'OFFLOAD_IMMEDIATE', False)


def enable(func):
    """
    Decorator that adds <func>.offload(request, [...], [optional kwargs]).

    Example usage:
        myfunc.offload(request, success_message="Done!", toast_position="bottom-left")
    If user calls .offload() with no extra kwargs, we use defaults.
    """

    def offload(*args, **kwargs):
        # If OFFLOAD_IMMEDIATE = True, run immediately (synchronous) for debugging
        if OFFLOAD_IMMEDIATE:
            func(*args, **kwargs)
            return None

        success_message = kwargs.pop('success_message', None)
        fail_message = kwargs.pop('fail_message', None)
        message_duration = kwargs.pop('message_duration', None)

        # New optional UI fields
        toast_position = kwargs.pop('toast_position', None)
        color_code = kwargs.pop('color_code', None)

        # Create the OffloadTask in PENDING
        task = OffloadTask.objects.create(
            status=OffloadTask.STATUS_PENDING,
            success_message=success_message,
            fail_message=fail_message,
            message_duration=message_duration,
            toast_position=toast_position,
            color_code=color_code
        )

        kwargs['__task_id__'] = str(task.id)

        # If first arg is request, store user
        if args and hasattr(args[0], 'user'):
            req = args[0]
            if req.user and req.user.is_authenticated:
                task.user = req.user
                task.save(update_fields=['user'])

        # Add to in-memory queue
        function_queue.append((func, args, kwargs, str(task.id)))

        # Also store the task ID in request._offload_task_ids if present
        if args and hasattr(args[0], 'META'):
            request = args[0]
            if hasattr(request, '_offload_task_ids'):
                request._offload_task_ids.append(str(task.id))

        return str(task.id)

    func.offload = offload
    return func
