from datetime import datetime

# from app.tasks import launch
from random import Random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
# Create your views here.
from workflows.models import Workflow, Task, TaskBase, Subtask, SubtaskBase


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


def workflow_view(request, id):
    context = {"workflow": list(Workflow.objects.filter(id=id))[0]}
    return render(request, 'pages/workflow.html', context)


def update_create_workflow_view(request):
    if request.method == "POST":
        name_workflow = request.POST.get('name_workflow')
        description_workflow = request.POST.get('description_workflow')
        # skip_workflow = bool(request.POST.get('skip_workflow'))
        # previous_workflow = bool(request.POST.get('previous_workflow'))
        tasks_base = [TaskBase.objects.filter(id=x)[0] for x in request.POST.keys() if x.isdigit()]
        tasks = []
        for task_base in tasks_base:
            subtasks = []
            for subtask_base in task_base.subtasks.all():
                subtasks.append(Subtask.objects.create(name=subtask_base.name,
                                                       notes=subtask_base.notes,
                                                       script_path=subtask_base.script_path,
                                                       created_on=subtask_base.created_on,
                                                       updated_on=datetime.now,
                                                       skip=subtask_base.skip,
                                                       run_with_previous=subtask_base.run_with_previous))
            task = Task.objects.create(
                name=task_base.name,
                notes=task_base.notes,
                created_on=task_base.created_on,
                updated_on=datetime.now,
                skip=task_base.skip,
                run_with_previous=task_base.run_with_previous
            )
            task.subtasks.set(subtasks)
            task.save()
            tasks.append(task)
        # TODO add custom response
        if not tasks:
            return HttpResponse(status=400)
        workflow = Workflow.objects.create(name=name_workflow,
                                           notes=description_workflow,
                                           # skip=skip_workflow,
                                           # run_with_previous=previous_workflow,
                                           author=request.user)
        workflow.tasks.set(tasks)
        workflow.users.set(list(User.objects.all()))
        workflow.save()
        return redirect('/workflows')

    context = {
        'is_update': False,
        'title': 'Create workflow',
        'tasks': TaskBase.objects.all(),
    }
    return render(request, 'pages/create_workflow.html', context)


def update_create_task_view(request):
    if request.method == "POST":
        name_task = request.POST.get('name_task')
        description_task = request.POST.get('description_task')
        skip_task = bool(request.POST.get('skip_task'))
        previous_task = bool(request.POST.get('previous_task'))
        subtasks = [SubtaskBase.objects.filter(id=x)[0] for x in request.POST.keys() if x.isdigit()]
        # TODO add custom response
        if not subtasks:
            return HttpResponse(status=400)
        task = TaskBase.objects.create(name=name_task,
                                       notes=description_task,
                                       skip=skip_task,
                                       run_with_previous=previous_task)
        task.subtasks.set(subtasks)
        task.save()
        return redirect('/workflows')
    context = {
        'title': 'Create task',
        'subtasks': SubtaskBase.objects.all()
    }
    return render(request, 'pages/create_task.html', context)


def account_view(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if check_password(old_password, request.user.password):
            if new_password == confirm_password:
                updated_user = request.user
                updated_user.set_password(new_password)
                updated_user.save()
                return redirect('/login')
    return render(request, 'pages/account.html')


def logout_view(request):
    logout(request)
    return redirect('/login')


def delete_users_from_workflow_view(request, id):
    print("Work in progress")
    # TODO Add removing users from workflow


def workflow_start_view(request, id):
    ids = request.POST.get('ids')
    workflow = list(Workflow.objects.filter(id=id))[0]

    response = []
    tasks = []
    tasks_with_prev = []
    for task in workflow.tasks.all():
        print(task)
        if not task.skip:
            if task.run_with_previous:
                tasks_with_prev.append(task)
            else:
                if tasks_with_prev:
                    tasks.append(tasks_with_prev)
                tasks_with_prev = [task]
    tasks.append(tasks_with_prev)

    subtasks = []
    for tasks_prev in tasks:
        subtask_with_prev = []
        for task in tasks_prev:
            for subtask in task.subtasks.all():
                if not subtask.skip:
                    if subtask.run_with_previous:
                        subtask_with_prev.append(subtask)
                    else:
                        if subtask_with_prev:
                            subtasks.append(subtask_with_prev)
                        subtask_with_prev = [subtask]
        subtasks.append(subtask_with_prev)
        # for subtask in task.subtasks.all():
        #     if not subtask.skip:
        #         if subtask.run_with_previous:
        #             res = launch.delay({
        #                 'script': subtask.script_path
        #             })
        #         else:
        #             res = launch.delay({
        #                 'script': subtask.script_path
        #             })
        #             # res.get()
        #         # print(task, subtask, res.status)
        #         response.append(res)
    # print("Response", response)
    return HttpResponse('STARTED', status=200)


def workflow_update_view(request):
    body = eval(request.body)

    if body['type'] == 'subtask':
        obj = list(Subtask.objects.filter(id=body['id']))[0]
    elif body['type'] == 'task':
        obj = list(Task.objects.filter(id=body['id']))[0]

    if body['update'] == 'skip':
        obj.skip = not obj.skip
    elif body['update'] == 'previous':
        obj.run_with_previous = not obj.run_with_previous
    obj.save()
    return HttpResponse('Update', status=200)


def workflow_status_view(request):
    body = eval(request.body)
    return HttpResponse("cos dla usera: " + body['idUser'] + ' ' + str(Random().randint(0, 100)), 200)
