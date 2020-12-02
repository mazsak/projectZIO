from django.contrib import admin

from .models import SubtaskBase, Subtask, TaskBase, Task, Workflow, Dictionary

# Register your models here.
admin.site.register(SubtaskBase)
admin.site.register(Subtask)
admin.site.register(TaskBase)
admin.site.register(Task)
admin.site.register(Workflow)
admin.site.register(Dictionary)
