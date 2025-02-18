# django_offload_with_logs/apps.py

from django.apps import AppConfig

class DjangoOffloadWithLogsConfig(AppConfig):
    name = 'django_offload_with_logs'  # rename here

    def ready(self):
        import django_offload_with_logs.signals
