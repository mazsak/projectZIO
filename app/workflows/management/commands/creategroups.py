from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission, User
from django.db.utils import OperationalError
from django.db import IntegrityError, transaction


class Command(BaseCommand):
    help = 'Creates User and Workflow Manager groups and gives them proper permissions.'

    BASIC_USER_PERMISSIONS = [
        "change_workflow",
        "delete_workflow",
        "execute_workflow",
        "view_dictionary",
        "view_subtask",
        "view_task",
        "view_workflow",
    ]

    WORKFLOW_MANAGER_PERMISSIONS = BASIC_USER_PERMISSIONS + [
        "add_subtask",
        "add_task",
        "add_workflow",
        "assign_workflow",
        "change_task",
        "delete_subtask",
        "edit_subtask",
        "edit_task",
        "upload_script",
    ]
    
    
    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                assert Permission.objects.all()
                self.create_user_group()
                self.create_manager_group()
        except (AssertionError, OperationalError):
            raise CommandError("Permission table is empty! Try making migrations and then migrate models to database first!")
        except IntegrityError as err:
            raise CommandError("An error occured. " + err)

        self.stdout.write(self.style.SUCCESS('Successfully created User and Workflow Manager and gave them default permissions!'))
    
    
    def create_user_group(self):
        user_group, created = Group.objects.get_or_create(name="User")
        if created:
            user_permissions = Permission.objects.filter(
                codename__in=self.BASIC_USER_PERMISSIONS
            )
            
            user_group.permissions.set(user_permissions)
            user_group.save()
        else:
            raise CommandError("User group already exists!")
    
    
    def create_manager_group(self):
        manager_group, created = Group.objects.get_or_create(name="Workflow Manager")
        if created:
            manager_permissions = Permission.objects.filter(
                codename__in=self.WORKFLOW_MANAGER_PERMISSIONS
            )
            
            manager_group.permissions.set(manager_permissions)
            manager_group.save()
        else:
            raise CommandError("Workflow Manager group already exists!")
        