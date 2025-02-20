# django_offload_with_logs/migrations/0002_add_extra_fields.py
import django.db.models.deletion
from django.db import migrations, models
import django.conf
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('django_offload_with_logs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offloadtask',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=django.conf.settings.AUTH_USER_MODEL,
                verbose_name='User who triggered'
            ),
        ),
        migrations.AddField(
            model_name='offloadtask',
            name='start_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='offloadtask',
            name='end_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='offloadtask',
            name='toast_position',
            field=models.CharField(
                blank=True,
                help_text="Where to show toast (e.g. 'top-right', 'bottom-left')",
                max_length=50,
                null=True
            ),
        ),
        migrations.AddField(
            model_name='offloadtask',
            name='color_code',
            field=models.CharField(
                blank=True,
                help_text='Hex color code for toast background, e.g. #FF0000',
                max_length=7,
                null=True
            ),
        ),
    ]
