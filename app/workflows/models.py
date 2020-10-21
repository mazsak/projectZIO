from datetime import datetime

from django.conf import settings
from django.db import models


STATUS_VALUES = (
    ('ready', 'Ready to run'),
    ('running', 'Running right now'),
    ('halted', 'Halted running'),
    ('in_queue', 'Waiting in queue'),
    ('skipped', 'Skipped running'),
    ('failed', 'Failed to run'),
)


# Create your models here.
class Subtask(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    notes = models.CharField(max_length=1000)
    script_path = models.FilePathField()
    created_on = models.DateTimeField(default=datetime.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=32, choices=STATUS_VALUES,
        default='ready')

class Task(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    notes = models.CharField(max_length=1000)
    created_on = models.DateTimeField(default=datetime.now)
    updated_on = models.DateTimeField(auto_now=True)
    subtasks = models.ManyToManyField(Subtask)
    status = models.CharField(max_length=32, choices=STATUS_VALUES,
        default='ready')

class Workflow(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='author')
    name = models.CharField(max_length=60)
    notes = models.CharField(max_length=1000)
    created_on = models.DateTimeField(default=datetime.now)
    updated_on = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name='users')
    status = models.CharField(max_length=32, choices=STATUS_VALUES,
        default='ready')