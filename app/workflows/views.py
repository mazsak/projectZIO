from django.shortcuts import render
from django.contrib import messages


# Create your views here.

def index(request):
    return render(request, 'pages/index.html')


def login(request):
    username = request.POST.get('login')
    password = request.POST.get('password')
    # TODO: handle logging(check if user exists etc.)
    context = {
        'login': None,
        'password': None
    }
    # TODO: handle error messages
    # negative message
    messages.error(request, "Username or password not correct")
    #  positive message
    messages.info(request, "Account created successfully")
    return render(request, 'pages/login.html', context)


def register(request):
    username = request.POST.get('login')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    # TODO: handle registering
    context = {
        'login': None,
        'email': None,
        'password': None,
        'confirm_password': None
    }
    # TODO: handle error messages
    messages.error(request, "Username is already taken")
    return render(request, 'pages/register.html')
