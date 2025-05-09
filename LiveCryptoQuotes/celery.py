from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LiveCryptoQuotes.settings")
app = Celery("LiveCryptoQuotes")
app.conf.enable_utc = False
app.conf.update(timezone="Asia/Dhaka")
app.config_from_object("django.conf:settings", namespace="CELERY")


app.autodiscover_tasks()


def debug_task(self):
    print(f"Request: {self.request!r}")
