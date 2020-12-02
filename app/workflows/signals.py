from django.contrib.auth.models import Group, Permission, User  

__BASIC_USER_PERMISSIONS = [
    "view_workflow",
]

__WORKFLOW_MANAGER_PERMISSIONS = __BASIC_USER_PERMISSIONS + [
    "execute_workflow",
    "assign_workflow",
]


def populate_groups_and_permissions(sender, **kwargs):
    
    assert Permission.objects.all()
    
    # User Group
    user_group, created = Group.objects.get_or_create(name="User")
    if created:
        user_permissions = Permission.objects.filter(
            codename__in=__BASIC_USER_PERMISSIONS
        )
        
        user_group.permissions.set(user_permissions)
        user_group.save()
    
    # Workflow Manager Group
    manager_group, created = Group.objects.get_or_create(name="Workflow Manager")
    if created:
        manager_permissions = Permission.objects.filter(
            codename__in=__WORKFLOW_MANAGER_PERMISSIONS
        )
        
        manager_group.permissions.set(manager_permissions)
        manager_group.save()