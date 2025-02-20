# django_offload_with_logs/templatetags/offload_tags.py

from django import template
from django.urls import reverse
from django.templatetags.static import static
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.simple_tag(takes_context=True)
def offload_js(context):
    request = context.get('request')
    if not request:
        return ''

    # We'll read task IDs from session
    task_ids = request.session.get('offload_task_ids', [])
    task_ids_json = json.dumps(task_ids)

    # Build the base URL for 'offload_status'
    base_url = reverse('offload_status', kwargs={'task_id': '00000000-0000-0000-0000-000000000000'})
    base_url = base_url.replace('task-status/00000000-0000-0000-0000-000000000000/', '')

    poller_js = static('django_offload_with_logs/offload_js.js')

    script = f"""
<script>
    var OFFLOAD_TASK_IDS = {task_ids_json};
    var OFFLOAD_BASE_URL = '{base_url}';
</script>
<script src="{poller_js}"></script>
"""
    return mark_safe(script)
