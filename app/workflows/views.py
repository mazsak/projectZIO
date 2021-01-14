import os
from datetime import datetime

from app.celery import app
from app.tasks import fake_task, launch_subtask
from celery import chain, group
from celery.result import GroupResult
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
# Create your views here.
from workflows.models import Workflow, Task, TaskBase, Subtask, SubtaskBase


def index_view(request):
    return redirect('/workflows')


def login_view(request):
    if request.method == 'OPTIONS' and request.user.is_authenticated():
        return
    username = request.POST.get('login')
    password = request.POST.get('password')
    context = {
        'login': None,
        'password': None
    }
    user = authenticate(request, username=username, password=password)
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
    context = {
        'login': None,
        'email': None,
        'password': None,
        'confirm_password': None
    }
    if request.method == 'POST':
        check_user = User.objects.get(username=username)
        if check_user is not None:
            messages.error(request, "Username is already taken")
        else:
            user = User.objects.create_user(username, email, password)
            user.groups.add(Group.objects.get(name="User"))
            messages.success(request, "Account created successfully")
            return redirect('/login')
    return render(request, 'pages/register.html', context)

@login_required
def admin_file_view(request):
    if request.method == 'POST' and request.FILES['my_file']:
        fs = FileSystemStorage(location=os.path.join(os.getcwd(), 'skrypty'))
        file = request.FILES['my_file']
        filename = fs.save(file.name, file)
        return render(request, 'pages/account.html')
    return render(request, 'pages/add_file.html')


@login_required
@permission_required("workflows.view_workflow", raise_exception=True)
def workflows_view(request):
    logged_in_user = request.user
    context = {"workflows": Workflow.objects.filter(users=logged_in_user)}
    return render(request, 'pages/workflows.html', context)


@login_required
@permission_required("workflows.view_workflow", raise_exception=True)
def workflow_view(request, id):
    context = {"workflow": list(Workflow.objects.filter(id=id))[0]}
    return render(request, 'pages/workflow.html', context)

@login_required
def update_workflow_view(request, id):
    if request.method == "POST":
        workflow = Workflow.objects.get(id=request.POST.get('id_workflow'))
        workflow.name = request.POST.get('name_workflow')
        workflow.notes = request.POST.get('description_workflow')
        for task in workflow.tasks.all():
            Task.objects.filter(id=task.id).delete()
        tasks_base = [TaskBase.objects.filter(id=x)[0] for x in request.POST.keys() if x.isdigit()]
        tasks = []
        for task_base in tasks_base:
            subtasks = []
            for subtask_base in task_base.subtasks.all():
                subtask = Subtask.objects.create(name=subtask_base.name, notes=subtask_base.notes,
                                                 script_path=subtask_base.script_path,
                                                 created_on=subtask_base.created_on, updated_on=datetime.now,
                                                 skip=subtask_base.skip,
                                                 run_with_previous=subtask_base.run_with_previous)
                subtask.args.set(subtask_base.args.all())
                subtasks.append(subtask)
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
        workflow.tasks.set(tasks)
        workflow.updated_on = datetime.now()
        workflow.save()
        return redirect('/workflows')
    workflow = Workflow.objects.get(id=id)
    context = {
        'is_update': True,
        'title': 'Create workflow',
        'tasks': TaskBase.objects.all(),
        'selected_tasks': [select_task.name for select_task in workflow.tasks.all()],
        'workflow': workflow
    }
    return render(request, 'pages/create_workflow.html', context)


@login_required
@permission_required("workflows.change_workflow", raise_exception=True)
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
                subtask = Subtask.objects.create(name=subtask_base.name, notes=subtask_base.notes,
                                                script_path=subtask_base.script_path,
                                                created_on=subtask_base.created_on, updated_on=datetime.now,
                                                skip=subtask_base.skip,
                                                run_with_previous=subtask_base.run_with_previous)
                subtask.args.set(subtask_base.args.all())
                subtasks.append(subtask)
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
        workflow.users.set([request.user])
        workflow.updated_on = datetime.now()
        workflow.save()
        return redirect('/workflows')

    context = {
        'is_update': False,
        'title': 'Create workflow',
        'tasks': TaskBase.objects.all(),
    }
    return render(request, 'pages/create_workflow.html', context)


@login_required
@permission_required("workflows.add_task", raise_exception=True)
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
    context = {
        'is_great_group': request.user.groups.filter(name='Workflow Manager').exists()
    }
    return render(request, 'pages/account.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('/login')


@login_required
@permission_required("workflows.execute_workflow", raise_exception=True)
def workflow_start_view(request, id):
    ids = eval(request.body)['ids']
    workflow = list(Workflow.objects.filter(id=id))[0]
    celery_task_ids = {}
    workflow.updated_on = datetime.now()
    workflow.save()
    for user_id in ids:
        with open(f"log_{id}_{user_id}.txt", "a") as f:
            f.write(f"\nWorkflow date: {workflow.updated_on}\n")
        tasks = []
        tasks_with_prev = []
        for task in workflow.tasks.all():
            task_id = task.id
            if not task.skip:
                task.status = "PENDING"
                subtasks = []
                subtasks_with_prev = []
                for subtask in task.subtasks.all():
                    if not subtask.skip:
                        subtask.status = 'PENDING'
                        if subtask.run_with_previous:
                            subtasks_with_prev.append(subtask)
                        else:
                            if subtasks_with_prev:
                                subtasks.append(fake_task.s())
                                subtasks.append(
                                    group(launch_subtask.s(
                                        data={
                                            'id': subtask.id,
                                            'workflow_id': workflow.id,
                                            'task_id': task_id,
                                            'user_id': user_id
                                        }) for subtask in subtasks_with_prev))
                            subtasks_with_prev = [subtask]
                    else:
                        subtask.status = 'SKIPPED'
                    subtask.save()
                subtasks.append(fake_task.s())
                subtasks.append(group(
                    launch_subtask.s(data={
                        'id': subtask.id,
                        'workflow_id': workflow.id,
                        'task_id': task_id,
                        'user_id': user_id
                    }) for subtask in subtasks_with_prev))
                if task.run_with_previous:
                    tasks_with_prev.append(subtasks)
                else:
                    if tasks_with_prev:
                        tasks.append(fake_task.s())
                        tasks.append(group(chain(*sub) for sub in tasks_with_prev))
                    tasks_with_prev = [subtasks]
            else:
                task.status = "SKIPPED"
                for subtask in task.subtasks.all():
                    subtask.status = 'SKIPPED'
                    subtask.save()
            task.save()
        tasks.append(fake_task.s())
        tasks.append(group(chain(*sub) for sub in tasks_with_prev))
        ch = chain(*tasks)()
        celery_task_ids[user_id] = as_list(ch)

    workflow.celery_id = str(celery_task_ids)
    workflow.save()

    return HttpResponse(f'\n\n\nids: {ids}\n\n\n', status=200)


def as_list(task):
    results = []
    parent = task.parent
    if isinstance(task, GroupResult):
        for t in task.results:
            results.extend(as_list(t))
    else:
        results.append({'id': task.id, 'args': task.kwargs, 'esss': 'tuuuu'})
    if parent is not None:
        results.extend(as_list(parent))
    return results


@login_required
@permission_required("workflows.execute_workflow", raise_exception=True)
def workflow_stop_view(request, id):
    ids = eval(request.body)['ids']
    workflow = Workflow.objects.filter(id=id)[0]
    task_ids = eval(workflow.celery_id)
    for user_id in ids:
        for task_id in task_ids[user_id]:
            app.control.revoke(task_id['id'], terminate=True, signal='SIGKILL')
        with open(f'log_{id}_{user_id}.txt', 'a') as f:
            f.write("\nWorkflow has been stopped\n")

    return HttpResponse('Stop', status=200)


@login_required
@permission_required("workflows.change_workflow", raise_exception=True)
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
    response = []
    workflow = list(Workflow.objects.filter(id=body['id']))[0]
    tasks = workflow.tasks.all()
    current_line = 'Workflow date: '
    try:
        with open(f'log_{body["id"]}_{body["idUser"]}.txt', 'r') as f:
            lines = f.readlines()
            index = [lines.index(line) for line in lines if line.startswith(current_line)][-1]
            lines = lines[index:]
            subtasks_ids = list(
                {int(line.replace('Subtask id: ', '')) for line in lines if line.startswith("Subtask id: ")})
            for task in tasks:
                if task.skip:
                    response.append({"id": task.id, "action": "skip"})
                else:
                    counter = 0
                    subtasks = task.subtasks.all()
                    ids = [subtask.id for subtask in subtasks if not subtask.skip]
                    for subtask_id in subtasks_ids:
                        if subtask_id in ids:
                            counter += 1
                    if counter == len(ids):
                        response.append({"id": task.id, "action": "finished"})
                    elif counter == 0:
                        response.append({"id": task.id, "action": "queue"})
                    else:
                        response.append({"id": task.id, "action": "started"})
        return HttpResponse(str(response), status=200)
    except Exception as e:
        response = [{"id": task.id, "action": "queue", 'try': str(e)} for task in tasks]
        return HttpResponse(str(response), status=200)

@login_required
def workflow_log_view(request, file):
    with open(file, 'r') as f:
        return HttpResponse(f.read(), content_type='text/plain')
