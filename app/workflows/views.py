from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from workflows.models import Workflow


def index_view(request):
    return render(request, 'pages/index.html')


def login_view(request):
    username = request.POST.get('login')
    password = request.POST.get('password')
    context = {
        'login': None,
        'password': None
    }
    user = authenticate(request, username=username, password=password)
    # print(request.META.get('HTTP_REFERER'))
    if request.method == 'GET':
        if user is not None:
            messages.info(request, "Account created successfully")
    elif request.method == 'POST':
        if user is not None:
            login(request, user)
            messages.info(request, "Logged in successfully")
            return redirect('/workflows')
        else:
            messages.error(request, "Username or password not correct")
    return render(request, 'pages/login.html', context)


def register_view(request):
    username = request.POST.get('login')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    context = {
        'login': None,
        'email': None,
        'password': None,
        'confirm_password': None
    }
    if request.method == 'POST':
        check_user = authenticate(username=username, password=password)
        if check_user is not None:
            messages.error(request, "Username is already taken")
        else:
            user = User.objects.create_user(username, email, password)
            messages.success(request, "Account created successfully")
            return redirect('/workflows')
    return render(request, 'pages/register.html', context)


def workflows_view(request):
    logged_in_user = request.user
    context = {"workflows": Workflow.objects.filter(author=logged_in_user)}
    return render(request, 'pages/workflows.html', context)


def update_create_workflow_view(request):
    context = {
        'title': 'Create workflow'
    }
    return render(request, 'pages/create_workflow.html', context)
