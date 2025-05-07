import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import stock_app.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LiveStockTracker.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # Add WebSocket URL routing here if needed
        "websocket": AuthMiddlewareStack(
            URLRouter(
                stock_app.routing.websocket_urlpatterns
            )  # Replace with your WebSocket URL routing
        ),
    }
)
