from subprocess import Popen, PIPE, STDOUT

from celery import shared_task, chain, group

from workflows.models import Task, Subtask


@shared_task(bind=True)
def launch_subtask(self, data):
    res = []
    subtask = list(Subtask.objects.filter(id=data['subtask_id']))[0]
    subtask.status = 'STARTED'
    subtask.save()
    process = Popen(
        f"/usr/src/nextflow run {subtask.script_path}",
        bufsize=1,
        stdout=PIPE,
        stderr=STDOUT,
        stdin=PIPE,
        shell=True
    )

    for line in iter(process.stdout.readline, b''):
        line = line.decode('utf-8')
        res.append(line)
        print(line)
    process.wait()
    subtask.status = 'SUCCESS'
    subtask.save()
    return res


@shared_task(bind=True)
def launch_task(self, data):
    responses = []
    res = []

    task = list(Task.objects.filter(id=data['task_id']))[0]
    task.status = 'STARTED'
    task.save()
    subtasks = []
    subtasks_with_prev = []
    for subtask in task.subtasks.all():
        if not subtask.skip:
            if subtask.run_with_previous:
                subtasks_with_prev.append(subtask)
            else:
                if subtasks_with_prev:
                    subtasks.append(subtasks_with_prev)
                subtasks_with_prev = [subtask]
    subtasks.append(subtasks_with_prev)

    for subtasks_group in subtasks:
        for subtask in subtasks_group:
            subtask.status = 'PENDING'
            subtask.save()
    ch = chain(*[group(*[launch_task.s({'subtask_id': subtask.id}) for subtask in subtasks_group]) for subtasks_group in subtasks]).apply_async()

    task.status = 'SUCCESS'
    task.save()
    return res