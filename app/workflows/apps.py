from django.apps import AppConfig
from django.db.models.signals import post_migrate


class WorkflowsConfig(AppConfig):
    name = 'workflows'

    def ready(self):
        from .signals import populate_groups_and_permissions
        post_migrate.connect(populate_groups_and_permissions, sender=self)