import os
from datetime import datetime

from django.conf import settings
from django.db import models

STATUS_VALUES = (
    ('READY', 'Ready to run'),
    ('STARTED', 'Running right now'),
    ('HALTED', 'Halted running'),
    ('PENDING', 'Waiting in queue'),
    ('SKIPPED', 'Skipped running'),
    ('FAILURE', 'Failed to run'),
    ('SUCCESS', 'Finished successfully'),
)


class Dictionary(models.Model):
    argument = models.CharField(max_length=100)
    eval_str = models.CharField(max_length=100)

    def __str__(self):
        return self.argument


class SubtaskBase(models.Model):
    name = models.CharField(max_length=60)
    notes = models.CharField(max_length=1000)
    script_path = models.FilePathField(path=os.path.join(os.getcwd(), 'skrypty'))
    created_on = models.DateTimeField(default=datetime.now)
    updated_on = models.DateTimeField(auto_now=True)
    args = models.ManyToManyField(Dictionary, null=True)
    skip = models.BooleanField(default=False)
    run_with_previous = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class TaskBase(models.Model):
    name = models.CharField(max_length=60)
    notes = models.CharField(max_length=1000)
    created_on = models.DateTimeField(default=datetime.now)
    updated_on = models.DateTimeField(auto_now=True)
    subtasks = models.ManyToManyField(SubtaskBase)
    skip = models.BooleanField(default=False)
    run_with_previous = models.BooleanField(default=False)
    def __str__(self):
        return self.name


# Create your models here.
class Subtask(models.Model):
    
    class Meta:
        permissions = [
            ("upload_script", "Can upload script to subtask"),
        ]
    
    name = models.CharField(max_length=60)
    notes = models.CharField(max_length=1000)
    script_path = models.FilePathField(path=os.path.join(os.getcwd(), 'skrypty'))
    created_on = models.DateTimeField(default=datetime.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=32, choices=STATUS_VALUES,
                              default='READY')
    args = models.ManyToManyField(Dictionary, null=True)
    skip = models.BooleanField(default=False)
    run_with_previous = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=60)
    notes = models.CharField(max_length=1000)
    created_on = models.DateTimeField(default=datetime.now)
    updated_on = models.DateTimeField(auto_now=True)
    subtasks = models.ManyToManyField(Subtask)
    status = models.CharField(max_length=32, choices=STATUS_VALUES,
                              default='READY')
    skip = models.BooleanField(default=False)
    run_with_previous = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Workflow(models.Model):
    
    class Meta:
        permissions = [
            ("execute_workflow", "Can execute workflow's all tasks and subtasks"),
            ("assign_workflow", "Can assign workflow for user")
        ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='author')
    name = models.CharField(max_length=60)
    notes = models.CharField(max_length=1000)
    created_on = models.DateTimeField(default=datetime.now)
    updated_on = models.DateTimeField(default=datetime.now)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='users')
    tasks = models.ManyToManyField(Task)
    status = models.CharField(max_length=32, choices=STATUS_VALUES,
                              default='READY')
    celery_id = models.TextField(null=True)

    def __str__(self):
        return self.name
