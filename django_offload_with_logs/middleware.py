# django_offload_with_logs/middleware.py
from django.utils.deprecation import MiddlewareMixin

class OffloadMiddleware(MiddlewareMixin):
    """
    Captures newly scheduled task_ids and stores them in session for polling.
    """
    def process_request(self, request):
        request._offload_task_ids = []

    def process_response(self, request, response):
        if hasattr(request, '_offload_task_ids'):
            session_task_ids = request.session.get('offload_task_ids', [])
            for tid in request._offload_task_ids:
                if tid not in session_task_ids:
                    session_task_ids.append(tid)
            request.session['offload_task_ids'] = session_task_ids
        return response