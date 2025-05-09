from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/crypto/(?P<symbol>[\w\-:]+)/$", consumers.CryptoConsumer.as_asgi()),
]
# at bottom of crypto_app/routing.py

