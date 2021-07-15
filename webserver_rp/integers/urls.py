from django.urls import path
from .views import index
##Se agrega el path y la funcion que
#  ejecutara para mostrar la pagina web
# esta funcion es creada
urlpatterns = [
     path('', index)
]