# django-offload-with-logs

A small tool that lets you schedule lightweight background tasks to run after the HTTP response is sent, **with** optional toast notifications in the frontend. This is perfect for offloading small or moderate tasks (e.g., updates, sending logs, quick DB modifications) without the overhead of Celery.

## Features

- **Minimal Setup**: Just install, add to `INSTALLED_APPS` and `MIDDLEWARE`, and you're done.
- **Toast Notifications**: Automatically show success/failure messages with a small pop-up.  
- **Lightweight**: No need for Celery or a separate queue unless you have large-scale or very long tasks.
- **Configurable Messages**: Pass custom success/fail messages and durations if you like.

## Installation

1. Install from PyPI:

```bash
pip install django_offload_with_logs
```
2. Add to INSTALLED_APPS in your Django settings.py:
```bash
INSTALLED_APPS = [
    ...
    'django_offload_with_logs',
    ...
]
```
3. Include the middleware in your MIDDLEWARE list:
```bash
MIDDLEWARE = [
    ...,
    'django.contrib.sessions.middleware.SessionMiddleware',  # ensures session support
    ...,
    'django_offload_with_logs.middleware.OffloadMiddleware',
]
```
4. Include the URLs in your main urls.py:
```bash
from django.urls import path, include

urlpatterns = [
    ...,
    path('django_offload_with_logs/', include('django_offload_with_logs.urls')),
]

```
5. Run migrations to create the OffloadTask model in your database:
```bash
python manage.py migrate

```
6. Load the template tag in your base template (e.g. base.html) and inject the JavaScript for polling & toast:

```bash 
{% load offload_tags %}

<!DOCTYPE html>
<html>
<head>
    ...
    {% offload_js %}
</head>
<body>
    ...
</body>
</html>

```
## Basic Usage

1. Decorate your function with @enable, which creates <function>.offload(...):

```bash 
from django_offload_with_logs.decorators import enable
import time

@enable
def do_something_long(request,**kwargs):
    time.sleep(10)  # Simulate a 10-second task
    print("Finished the background job!")

```
2. Call the decorated function in a view using .offload(...):
```bash
def my_view(request):
    # Schedule the task to run after the response
    do_something_long.offload(request)
    # Return immediately
    return HttpResponse("Task scheduled! You can keep browsing.")

```
3. Once the HTTP response completes, do_something_long runs in the background, and a toast will appear on the frontend when it finishes.

## Advanced Usage
a function that further customize the success/fail messages based on the logic inside it and not based on the view that it's been called from , by retrieving the task_id from the kwargs:
```bash
@enable
def my_big_task(request, data, **kwargs):
    # retrieve the offloaded task_id automatically:
    task_id = kwargs.get('__task_id__')  # a string like "0f5d476e-..."
    print("Got a hidden task_id:", task_id)

    # you can do your logic, and if you want to update success_message:
    from .models import OffloadTask
    try:
        # some heavy logic
        result_count = len(data)
        # dynamic update
        task = OffloadTask.objects.get(id=task_id)
        task.success_message = f"Processed {result_count} items successfully!"
        task.save(update_fields=['success_message'])
    except Exception as e:
        # or fail
        OffloadTask.objects.filter(id=task_id).update(fail_message=str(e))
        raise
```

## Custom Messages & Durations 
If you want different messages or timing or position or color, you can pass them as arguments to .offload(...):

```bash 
do_something_long.offload(
    request,
    success_message="Task finished successfully!",
    fail_message="Oops! Something went wrong.",
    message_duration=8000,  # 8 seconds
    toast_position="top-right",
    color_code="#AAFFCC",
)

```