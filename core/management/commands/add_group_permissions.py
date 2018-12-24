from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from guardian.shortcuts import assign_perm

from core.permissions import GroupPermissionSetter, INSTANCE


class Command(BaseCommand):
    """
    Use to add group permissions.
    """
    help = 'Add group permissions to them.'

    def handle(self, *args, **kwargs):
        total = 0
        for app, groups in GroupPermissionSetter.GROUP_PERMISSIONS.items():
            app_counter = 0
            for group, verbs in groups.items():
                print(f"Assigning '{app}' application's permissions for '{group}' group.")
                group = Group.objects.get(name=group)
                for verb, models in verbs.items():
                    for model in models:
                        permission_code = ('_'.join([verb, model, INSTANCE]))
                        assign_perm(f'{app}.{permission_code}', group)
                        print(f'Assigned permission: {app}.{permission_code}')
                        app_counter += 1
                        total += 1
            print(f'{app_counter} {app} group permissions assigned.')
        print(f'{total} group permissions assigned in total.')
