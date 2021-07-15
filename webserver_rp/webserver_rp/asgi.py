"""
ASGI config for webserver_rp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

#Imports para que funcionen los websocket
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
#importar para que tenga la ruta del websocket
from integers.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webserver_rp.settings')

application = ProtocolTypeRouter({
    #se asigna que ocurre cuando la ruta es http://
    'http':get_asgi_application(),
    #se asigna que ocurre cuando la ruta es ws://
    #se tiene un middleware
    'websocket':AuthMiddlewareStack(URLRouter(ws_urlpatterns))
    })
