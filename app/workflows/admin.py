from django.contrib import admin

from .models import Subtask, Task, Workflow, Dictionary

# Register your models here.
admin.site.register(Subtask)
admin.site.register(Task)
admin.site.register(Workflow)
admin.site.register(Dictionary)
