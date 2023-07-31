import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Proto2.settings")
app = Celery("Proto2", broker='redis://default:5bcce6315ccc45bdbfa832c9114e42f4@fly-proto2-redis.upstash.io')
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()