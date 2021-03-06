"""
WSGI config for abdcp_adapter project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys

PROJECT_DIR = os.path.realpath(
    os.path.join(
        os.path.dirname(__file__), '..'
    )
)
sys.path.insert(1, PROJECT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "abdcp_adapter.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
