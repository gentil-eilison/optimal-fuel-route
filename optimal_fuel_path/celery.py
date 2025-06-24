import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'optimal_fuel_path.settings')

app = Celery('optimal_fuel_path')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
