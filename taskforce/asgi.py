# taskforce/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat import routing as chat_routing  # Replace 'your_app' with your actual app name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskforce.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_routing.websocket_urlpatterns  # Ensure this points to your websocket routes
        )
    ),
})
