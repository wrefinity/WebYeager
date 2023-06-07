import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

# Create a new instance of Celery
app = Celery('yeager_ai')

# Load the Celery configuration from Django settings
app.config_from_object(settings, namespace='CELERY')

# Discover and autodiscover tasks from all registered apps
app.autodiscover_tasks()

