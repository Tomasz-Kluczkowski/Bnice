from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from guardian.shortcuts import assign_perm

from accounts.permissions import GROUP_PERMISSIONS, INSTANCE


class Command(BaseCommand):
    """
    Use to add group permissions.
    """
    help = 'Add group permissions to them.'

    def handle(self, *args, **kwargs):
        print('Assigning group permissions.')
        counter = 0
        for group, apps in GROUP_PERMISSIONS.items():
            group = Group.objects.get(name=group)
            for app, verbs in apps.items():
                for verb, models in verbs.items():
                    for model in models:
                        permission = ('_'.join([verb, model, INSTANCE]))
                        assign_perm(f"{app}.{permission}", group)
                        print(f'Assigned permission: {app}.{permission}')
                        counter += 1

        print(f'{counter} group permissions assigned.')
        print('Assigning group permissions complete.')

