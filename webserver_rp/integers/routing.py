from django.urls import path
#se agrega la funcion principal
from .consumers import WSConsumer
#se le asigna una ruta al websocket
ws_urlpatterns = [
    path('ws/test/',WSConsumer.as_asgi())
]