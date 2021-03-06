from subprocess import Popen, PIPE, STDOUT

from celery import shared_task
from workflows.models import *
from django.contrib.auth.models import User, Group


@shared_task(bind=True)
def fake_task(self, *args, **kwargs):
    print("FAKE TASK")


@shared_task(bind=True)
def launch_subtask(self, *args, **kwargs):
    data = kwargs.get('data', None)
    print(f'\n\n\n data in launch subtask: {data} \n\n\n')
    res = []
    subtask = list(Subtask.objects.filter(id=data['id']))[0]
    args = subtask.args.all()
    args_str = ''
    for arg in args:
        args_str += f" --{arg.argument[2:-1].lower()} '{str(eval(arg.eval_str))}'"

    subtask.status = 'STARTED'
    subtask.save()
    process = Popen(
        f"/usr/src/nextflow run {subtask.script_path}{args_str}",
        bufsize=1,
        stdout=PIPE,
        stderr=STDOUT,
        stdin=PIPE,
        shell=True
    )

    task = subtask.task_set.all()[0]

    with open(f"log_{data['workflow_id']}_{data['user_id']}.txt", "a") as f:
        f.write(
            f"\nTask id: {task.id}\nTask name: {task.name}\nSubtask id: {data['id']}\nSubtask name: {subtask.name}\n")
        for line in iter(process.stdout.readline, b''):
            line = line.decode('utf-8')
            res.append(line)
            f.write(line)
            print(line)
    process.wait()

    subtask.status = 'SUCCESS'
    subtask.save()

    return res
