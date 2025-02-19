# django_offload_with_logs/migrations/0001_initial.py

import uuid
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # If your app depends on another app's migration, you can add it here, like:
        # ('some_other_app', '0001_initial'),
        # For now, we'll assume no dependencies:
    ]

    operations = [
        migrations.CreateModel(
            name='OffloadTask',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)),
                ('status', models.CharField(default='PENDING', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('success_message', models.CharField(blank=True, max_length=200, null=True)),
                ('fail_message', models.CharField(blank=True, max_length=200, null=True)),
                (
                    'message_duration',
                    models.IntegerField(
                        blank=True,
                        help_text='Duration in ms',
                        null=True
                    )
                ),
            ],
        ),
    ]
