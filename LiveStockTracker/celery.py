from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LiveStockTracker.settings")
app = Celery("LiveStockTracker")
app.conf.enable_utc = False
app.conf.update(timezone="Asia/Dhaka")
app.config_from_object("django.conf:settings", namespace="CELERY")
# app.conf.beat_schedule = {
#     "every-10-seconds": {
#         "task": "stock_app.tasks.crypto_quotes",
#         "schedule": 10.0,
#         "args": (["BINANCE:BTCUSDT"],),
#     }
# }


app.autodiscover_tasks()


def debug_task(self):
    print(f"Request: {self.request!r}")
