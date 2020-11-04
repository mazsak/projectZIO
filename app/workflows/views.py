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
        'is_new_account': False,
        'failed': False,
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
    return render(request, 'pages/register.html')
