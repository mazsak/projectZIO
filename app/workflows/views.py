from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from celery import chain, group, signature
from app.tasks import launch_task
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
            user.groups.add(Group.objects.get(name="User"))
            messages.success(request, "Account created successfully")
            return redirect('/login')
    return render(request, 'pages/register.html', context)


@login_required
@permission_required("workflows.view_workflow", raise_exception=True)
def workflows_view(request):
    logged_in_user = request.user
    context = {"workflows": Workflow.objects.filter(users=logged_in_user)}
    return render(request, 'pages/workflows.html', context)


@login_required
def workflow_view(request, id):
    context = {"workflow": list(Workflow.objects.filter(id=id))[0]}
    return render(request, 'pages/workflow.html', context)


@login_required
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


@login_required
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


@login_required
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


@login_required
def delete_users_from_workflow_view(request, id):
    print("Work in progress")
    # TODO Add removing users from workflow


@login_required
def workflow_start_view(request, id):
    ids = request.POST.get('ids')
    workflow = list(Workflow.objects.filter(id=id))[0]

    # response = []
    tasks = []
    tasks_with_prev = []
    for task in workflow.tasks.all():
        if not task.skip:
            task.status = "PENDING"
            for subtask in task.subtasks.all():
                if not subtask.skip:
                    subtask.status = 'PENDING'
                else:
                    subtask.status = 'SKIPPED'
                subtask.save()
            if task.run_with_previous:
                tasks_with_prev.append(task)
            else:
                if tasks_with_prev:
                    tasks.append(tasks_with_prev)
                tasks_with_prev = [task]
        else:
            task.status = "SKIPPED"
            for subtask in task.subtasks.all():
                subtask.status = 'SKIPPED'
                subtask.save()
        task.save()
    tasks.append(tasks_with_prev)
    # group = 'chain('
    # for tasks_group in tasks:
    #     group += 'group(['
    #     for task in tasks_group:
    #         group += 'launch_task.s({"task_id":' + str(task.id) + '}), '
    #     group = group[:-2]
    #     group += '])(), '
    # group = group[:-2]
    # group += ').apply_async()'
    # print("\n\n\n", group, '\n\n\n')
    # eval(group)
    ch = chain(*[group(*[launch_task.s({'task_id': task.id}) for task in tasks_group]) for tasks_group in tasks])\
        .apply_async()

    return HttpResponse("g().get()", status=200)


@login_required
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


@login_required
def workflow_status_view(request):
    body = eval(request.body)
    response = {}
    for task in list(Workflow.objects.filter(id=body['id']))[0].tasks.all():
        if not task.skip:
            response[f'Task-{task.name}{task.id}'] = task.status
            for subtask in task.subtasks.all():
                if not subtask.skip:
                    response[f'{subtask.name}-{subtask.id}'] = subtask.status
    return HttpResponse(str(response), 200)
