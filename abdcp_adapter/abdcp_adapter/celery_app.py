from __future__ import absolute_import
import os
import sys

from django.conf import settings
from celery import Celery

# Indicate Celery to use the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abdcp_adapter.settings')

app = Celery('abdcp_adapter')
app.config_from_object('django.conf:settings')
# This line will tell Celery to autodiscover all your tasks.py that are in your app folders
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)