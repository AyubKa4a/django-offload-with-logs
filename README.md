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
def do_something_long(request):
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

## Custom Messages & Durations 
If you want different messages or timing:

```bash 
do_something_long.offload(
    request,
    success_message="Task finished successfully!",
    fail_message="Oops! Something went wrong.",
    message_duration=8000  # 8 seconds
)

```