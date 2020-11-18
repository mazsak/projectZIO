from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from workflows.models import Workflow, Task, Subtask


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
            return redirect('/login')
    return render(request, 'pages/register.html', context)


def workflows_view(request):
    logged_in_user = request.user
    context = {"workflows": Workflow.objects.filter(users=logged_in_user)}
    return render(request, 'pages/workflows.html', context)


def update_create_workflow_view(request):
    if request.method == "POST":
        name_workflow = request.POST.get('name_workflow')
        description_workflow = request.POST.get('description_workflow')
        skip_workflow = bool(request.POST.get('skip_workflow'))
        previous_workflow = bool(request.POST.get('previous_workflow'))
        tasks = [Task.objects.filter(id=x)[0] for x in request.POST.keys() if x.isdigit()]
        # TODO add custom response
        if not tasks:
            return HttpResponse(status=400)
        workflow = Workflow.objects.create(name=name_workflow,
                                           notes=description_workflow,
                                           skip=skip_workflow,
                                           run_with_previous=previous_workflow,
                                           author=request.user)
        workflow.tasks.set(tasks)
        workflow.users.set(list(User.objects.all()))
        workflow.save()
        return redirect('/workflows')

    context = {
        'is_update': False,
        'title': 'Create workflow',
        'tasks': Task.objects.all(),
    }
    return render(request, 'pages/create_workflow.html', context)


def update_create_task_view(request):
    if request.method == "POST":
        name_task = request.POST.get('name_task')
        description_task = request.POST.get('description_task')
        skip_task = bool(request.POST.get('skip_task'))
        previous_task = bool(request.POST.get('previous_task'))
        subtasks = [Subtask.objects.filter(id=x)[0] for x in request.POST.keys() if x.isdigit()]
        # TODO add custom response
        if not subtasks:
            return HttpResponse(status=400)
        task = Task.objects.create(name=name_task,
                                   notes=description_task,
                                   skip=skip_task,
                                   run_with_previous=previous_task)
        task.subtasks.set(subtasks)
        task.save()
        return redirect('/workflows')
    context = {
        'title': 'Create task',
        'subtasks': Subtask.objects.all()
    }
    return render(request, 'pages/create_task.html', context)

def logout_view(request):
    logout(request)
    return redirect('/login')