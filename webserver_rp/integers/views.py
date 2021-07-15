from django.shortcuts import render

# Create your views here.
# se crea una funcion que indica que se debe renderizar
# el template index.html
def index(request):
    return render(request, 'index.html')
