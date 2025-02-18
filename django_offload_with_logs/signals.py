# django_offload_with_logs/signals.py
import threading
import logging
from django.core.signals import request_finished
from django.conf import settings
from .store import function_queue
from .models import OffloadTask

logger = logging.getLogger(__name__)
OFFLOAD_RUN_ASYNC = getattr(settings, 'OFFLOAD_RUN_ASYNC', True)

def run_func(func, task_id, *args, **kwargs):
    task = OffloadTask.objects.get(pk=task_id)
    task.mark_running()
    try:
        func(*args, **kwargs)
        task.mark_success()
    except Exception as e:
        task.mark_failure()
        logger.exception("Error in offload task: %s", e)

def run_offloaded_tasks(sender, **kwargs):
    while function_queue:
        func, args, kw, task_id = function_queue.pop()
        if OFFLOAD_RUN_ASYNC:
            threading.Thread(target=run_func, args=(func, task_id, *args), kwargs=kw).start()
        else:
            run_func(func, task_id, *args, **kw)

request_finished.connect(run_offloaded_tasks)